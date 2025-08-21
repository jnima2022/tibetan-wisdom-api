from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import json
import random
from typing import Optional, List
from pydantic import BaseModel
import uvicorn

# Pydantic models for API responses
class Wisdom(BaseModel):
    id: int
    text: str
    author: str
    source: str
    category: str
    language: str

class WisdomResponse(BaseModel):
    wisdom: Wisdom

class WisdomListResponse(BaseModel):
    wisdom: List[Wisdom]
    total: int
    page: int
    per_page: int

class ApiInfo(BaseModel):
    name: str
    version: str
    description: str
    total_wisdom: int
    categories: List[str]
    authors: List[str]

# Rate limiting setup
limiter = Limiter(key_func=get_remote_address)

# Initialize FastAPI app
app = FastAPI(
    title="Tibetan Wisdom API",
    description="Access over 1000 pieces of authentic Tibetan wisdom from the Dalai Lama, Buddhist masters, and traditional teachings",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add rate limiting to app
app.state.limiter = limiter

# Custom rate limit exceeded handler
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    response = JSONResponse(
        status_code=429,
        content={
            "error": "Rate limit exceeded",
            "message": f"Too many requests. Limit: {exc.detail}",
            "retry_after": "Please wait before making more requests"
        }
    )
    response.headers["Retry-After"] = "60"
    return response

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load wisdom data
try:
    with open("tibetan_quotes_collection.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    wisdom_data = data["tibetan_quotes_collection"]["quotes"]
    metadata = data["tibetan_quotes_collection"]["metadata"]
except FileNotFoundError:
    wisdom_data = []
    metadata = {"total_quotes": 0, "categories": [], "sources": []}

# Extract unique values for filtering
categories = list(set(wisdom["category"] for wisdom in wisdom_data))
authors = list(set(wisdom["author"] for wisdom in wisdom_data))
sources = list(set(wisdom["source"] for wisdom in wisdom_data))

@app.get("/", response_class=HTMLResponse)
@limiter.limit("30/minute")
async def landing_page(request: Request):
    """Landing page with API documentation and examples"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Tibetan Wisdom Quotes API</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            .gradient-bg { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
            .code-block { background: #1a1a1a; }
        </style>
    </head>
    <body class="bg-gray-50">
        <!-- Hero Section -->
        <div class="gradient-bg text-white">
            <div class="container mx-auto px-6 py-20">
                <div class="text-center">
                    <h1 class="text-5xl font-bold mb-4">Tibetan Wisdom API</h1>
                    <p class="text-xl mb-8 opacity-90">Access over 1000 profound pieces of wisdom from Tibetan Buddhist masters and traditional teachings</p>
                    <div class="flex justify-center space-x-4">
                        <a href="/docs" class="bg-white text-purple-600 px-6 py-3 rounded-lg font-semibold hover:bg-gray-100 transition">
                            API Documentation
                        </a>
                        <button onclick="getRandomWisdom()" class="border-2 border-white text-white px-6 py-3 rounded-lg font-semibold hover:bg-white hover:text-purple-600 transition">
                            Try Random Wisdom
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Wisdom Display -->
        <div class="container mx-auto px-6 py-12">
            <div id="wisdom-display" class="hidden bg-white rounded-lg shadow-lg p-8 mb-12 border-l-4 border-purple-500">
                <blockquote class="text-xl italic text-gray-700 mb-4" id="wisdom-text"></blockquote>
                <cite class="text-gray-600 font-semibold" id="wisdom-author"></cite>
                <div class="text-sm text-gray-500 mt-2" id="wisdom-meta"></div>
            </div>
        </div>

        <!-- Features Section -->
        <div class="container mx-auto px-6 py-12">
            <h2 class="text-3xl font-bold text-center mb-12 text-gray-800">Features</h2>
            <div class="grid md:grid-cols-3 gap-8">
                <div class="text-center p-6">
                    <div class="bg-purple-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                        <svg class="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
                        </svg>
                    </div>
                    <h3 class="text-xl font-semibold mb-2">Rich Content</h3>
                    <p class="text-gray-600">1000+ authentic pieces of wisdom from the Dalai Lama, Buddhist texts, and traditional Tibetan teachings</p>
                </div>
                <div class="text-center p-6">
                    <div class="bg-purple-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                        <svg class="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                        </svg>
                    </div>
                    <h3 class="text-xl font-semibold mb-2">Smart Filtering</h3>
                    <p class="text-gray-600">Search by category, author, keyword, or get random inspirational wisdom</p>
                </div>
                <div class="text-center p-6">
                    <div class="bg-purple-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                        <svg class="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                        </svg>
                    </div>
                    <h3 class="text-xl font-semibold mb-2">Fast & Reliable</h3>
                    <p class="text-gray-600">Built with FastAPI for high performance and automatic API documentation</p>
                </div>
            </div>
        </div>

        <!-- API Endpoints Section -->
        <div class="bg-white py-12">
            <div class="container mx-auto px-6">
                <h2 class="text-3xl font-bold text-center mb-12 text-gray-800">API Endpoints</h2>
                <div class="grid md:grid-cols-2 gap-8">
                    <div class="border rounded-lg p-6">
                        <h3 class="text-xl font-semibold mb-3 text-purple-600">GET /wisdom/random</h3>
                        <p class="text-gray-600 mb-4">Get a random piece of wisdom</p>
                        <div class="code-block text-white p-4 rounded text-sm">
                            <div class="text-green-400">curl https://tibetan-wisdom-api.onrender.com/wisdom/random</div>
                        </div>
                    </div>
                    <div class="border rounded-lg p-6">
                        <h3 class="text-xl font-semibold mb-3 text-purple-600">GET /wisdom</h3>
                        <p class="text-gray-600 mb-4">Get paginated wisdom with optional filtering</p>
                        <div class="code-block text-white p-4 rounded text-sm">
                            <div class="text-green-400">curl https://tibetan-wisdom-api.onrender.com/wisdom?category=wisdom&page=1</div>
                        </div>
                    </div>
                    <div class="border rounded-lg p-6">
                        <h3 class="text-xl font-semibold mb-3 text-purple-600">GET /wisdom/categories</h3>
                        <p class="text-gray-600 mb-4">Get all available categories</p>
                        <div class="code-block text-white p-4 rounded text-sm">
                            <div class="text-green-400">curl https://tibetan-wisdom-api.onrender.com/wisdom/categories</div>
                        </div>
                    </div>
                    <div class="border rounded-lg p-6">
                        <h3 class="text-xl font-semibold mb-3 text-purple-600">GET /wisdom/search</h3>
                        <p class="text-gray-600 mb-4">Search wisdom by keyword</p>
                        <div class="code-block text-white p-4 rounded text-sm">
                            <div class="text-green-400">curl https://tibetan-wisdom-api.onrender.com/wisdom/search?q=compassion</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Rate Limits Section -->
        <div class="bg-gray-100 py-12">
            <div class="container mx-auto px-6">
                <h2 class="text-3xl font-bold text-center mb-8 text-gray-800">API Rate Limits</h2>
                <div class="max-w-4xl mx-auto bg-white rounded-lg shadow-lg p-8">
                    <p class="text-gray-600 mb-6 text-center">To ensure fair usage and optimal performance for all users, our API has the following rate limits:</p>
                    <div class="grid md:grid-cols-2 gap-6">
                        <div class="bg-blue-50 p-4 rounded">
                            <h4 class="font-semibold text-blue-800 mb-2">🎲 Random Wisdom</h4>
                            <p class="text-blue-600">30 requests per minute</p>
                        </div>
                        <div class="bg-green-50 p-4 rounded">
                            <h4 class="font-semibold text-green-800 mb-2">📖 Wisdom Listings</h4>
                            <p class="text-green-600">20 requests per minute</p>
                        </div>
                        <div class="bg-purple-50 p-4 rounded">
                            <h4 class="font-semibold text-purple-800 mb-2">🔍 Search</h4>
                            <p class="text-purple-600">15 requests per minute</p>
                        </div>
                        <div class="bg-gray-50 p-4 rounded">
                            <h4 class="font-semibold text-gray-800 mb-2">📊 Metadata</h4>
                            <p class="text-gray-600">10 requests per minute</p>
                        </div>
                    </div>
                    <div class="mt-6 p-4 bg-yellow-50 border-l-4 border-yellow-400 rounded">
                        <p class="text-yellow-800"><strong>Need higher limits?</strong> Contact us for enterprise API access or consider hosting your own instance!</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Use Cases Section -->
        <div class="py-12">
            <div class="container mx-auto px-6">
                <h2 class="text-3xl font-bold text-center mb-12 text-gray-800">Use Cases & Ideas</h2>
                <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
                    <div class="bg-white rounded-lg shadow-lg p-6 border-t-4 border-blue-500">
                        <div class="text-blue-500 text-3xl mb-4">📱</div>
                        <h3 class="text-xl font-semibold mb-3">Mobile Apps</h3>
                        <p class="text-gray-600">Send daily wisdom notifications to inspire your users with authentic Tibetan teachings.</p>
                    </div>
                    <div class="bg-white rounded-lg shadow-lg p-6 border-t-4 border-green-500">
                        <div class="text-green-500 text-3xl mb-4">🌐</div>
                        <h3 class="text-xl font-semibold mb-3">Website Headers</h3>
                        <p class="text-gray-600">Display rotating wisdom quotes in your website header to create a mindful user experience.</p>
                    </div>
                    <div class="bg-white rounded-lg shadow-lg p-6 border-t-4 border-purple-500">
                        <div class="text-purple-500 text-3xl mb-4">📧</div>
                        <h3 class="text-xl font-semibold mb-3">Email Signatures</h3>
                        <p class="text-gray-600">Add a touch of wisdom to your email communications with meaningful Buddhist quotes.</p>
                    </div>
                    <div class="bg-white rounded-lg shadow-lg p-6 border-t-4 border-orange-500">
                        <div class="text-orange-500 text-3xl mb-4">🧘</div>
                        <h3 class="text-xl font-semibold mb-3">Meditation Apps</h3>
                        <p class="text-gray-600">Integrate wisdom teachings into meditation sessions and mindfulness practices.</p>
                    </div>
                    <div class="bg-white rounded-lg shadow-lg p-6 border-t-4 border-pink-500">
                        <div class="text-pink-500 text-3xl mb-4">📚</div>
                        <h3 class="text-xl font-semibold mb-3">Educational Platforms</h3>
                        <p class="text-gray-600">Enhance learning experiences with profound teachings from Tibetan Buddhist masters.</p>
                    </div>
                    <div class="bg-white rounded-lg shadow-lg p-6 border-t-4 border-teal-500">
                        <div class="text-teal-500 text-3xl mb-4">💬</div>
                        <h3 class="text-xl font-semibold mb-3">Chatbots & AI</h3>
                        <p class="text-gray-600">Train AI assistants with authentic wisdom to provide meaningful, compassionate responses.</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- How to Use Section -->
        <div class="bg-gray-50 py-12">
            <div class="container mx-auto px-6">
                <h2 class="text-3xl font-bold text-center mb-12 text-gray-800">How to Get Started</h2>
                <div class="max-w-4xl mx-auto">
                    <div class="grid md:grid-cols-3 gap-8 mb-12">
                        <div class="text-center">
                            <div class="bg-blue-500 text-white w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">1</div>
                            <h3 class="text-lg font-semibold mb-2">Explore the API</h3>
                            <p class="text-gray-600">Visit our <a href="/docs" class="text-blue-500 hover:underline">interactive documentation</a> to see all available endpoints.</p>
                        </div>
                        <div class="text-center">
                            <div class="bg-green-500 text-white w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">2</div>
                            <h3 class="text-lg font-semibold mb-2">Make Your First Request</h3>
                            <p class="text-gray-600">Try our random wisdom endpoint to get started with your first API call.</p>
                        </div>
                        <div class="text-center">
                            <div class="bg-purple-500 text-white w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">3</div>
                            <h3 class="text-lg font-semibold mb-2">Integrate & Build</h3>
                            <p class="text-gray-600">Use our examples to integrate wisdom into your applications and projects.</p>
                        </div>
                    </div>
                    
                    <!-- Quick Examples -->
                    <div class="bg-white rounded-lg shadow-lg p-8">
                        <h3 class="text-2xl font-semibold mb-6 text-center">Quick Start Examples</h3>
                        <div class="grid md:grid-cols-2 gap-6">
                            <div>
                                <h4 class="font-semibold text-gray-800 mb-3">JavaScript/Node.js</h4>
                                <div class="code-block text-white p-4 rounded text-sm overflow-x-auto">
                                    <pre class="text-green-400 whitespace-pre-wrap break-words">fetch('https://tibetan-wisdom-api.onrender.com/wisdom/random')
.then(response => response.json())
.then(data => {
  console.log(data.wisdom.text);
});</pre>
                                </div>
                            </div>
                            <div>
                                <h4 class="font-semibold text-gray-800 mb-3">Python</h4>
                                <div class="code-block text-white p-4 rounded text-sm overflow-x-auto">
                                    <pre class="text-green-400 whitespace-pre-wrap break-words">import requests
response = requests.get('https://tibetan-wisdom-api.onrender.com/wisdom/random')
wisdom = response.json()['wisdom']
print(wisdom['text'])</pre>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- FAQ Section -->
        <div class="py-12">
            <div class="container mx-auto px-6">
                <h2 class="text-3xl font-bold text-center mb-12 text-gray-800">Frequently Asked Questions</h2>
                <div class="max-w-4xl mx-auto space-y-6">
                    <div class="bg-white rounded-lg shadow-lg p-6">
                        <h3 class="text-lg font-semibold mb-3 text-gray-800">Is this API free to use?</h3>
                        <p class="text-gray-600">Yes! Our API is completely free with rate limits to ensure fair usage. For higher limits or commercial use, please contact us.</p>
                    </div>
                    <div class="bg-white rounded-lg shadow-lg p-6">
                        <h3 class="text-lg font-semibold mb-3 text-gray-800">How accurate are these wisdom teachings?</h3>
                        <p class="text-gray-600">All wisdom pieces are sourced from authentic Tibetan Buddhist texts, teachings of the Dalai Lama, and traditional proverbs. We maintain high standards for authenticity and accuracy.</p>
                    </div>
                    <div class="bg-white rounded-lg shadow-lg p-6">
                        <h3 class="text-lg font-semibold mb-3 text-gray-800">Can I use this in my commercial application?</h3>
                        <p class="text-gray-600">Yes, you can use our API in commercial applications. Please respect the rate limits and consider reaching out for partnership opportunities if you need higher usage.</p>
                    </div>
                    <div class="bg-white rounded-lg shadow-lg p-6">
                        <h3 class="text-lg font-semibold mb-3 text-gray-800">How often is the content updated?</h3>
                        <p class="text-gray-600">We regularly review and expand our collection. Community contributions are welcome through our GitHub repository.</p>
                    </div>
                    <div class="bg-white rounded-lg shadow-lg p-6">
                        <h3 class="text-lg font-semibold mb-3 text-gray-800">What if I hit the rate limit?</h3>
                        <p class="text-gray-600">If you exceed the rate limit, you'll receive a 429 status code. Simply wait a minute before making more requests, or contact us for higher limits.</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Contribute Section -->
        <div class="bg-blue-50 py-12">
            <div class="container mx-auto px-6 text-center">
                <h2 class="text-3xl font-bold mb-6 text-gray-800">Help Grow Our Collection</h2>
                <p class="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
                    We believe wisdom should be shared. If you have authentic Tibetan wisdom teachings, traditional proverbs, 
                    or know of sources we should include, we'd love your contribution!
                </p>
                <div class="bg-white rounded-lg shadow-lg p-8 max-w-4xl mx-auto">
                    <h3 class="text-xl font-semibold mb-4 text-gray-800">Ways to Contribute</h3>
                    <div class="grid md:grid-cols-2 gap-4 text-left">
                        <div class="flex items-start space-x-3">
                            <div class="text-green-500 text-xl">✅</div>
                            <div>
                                <strong>Submit on GitHub:</strong> Create pull requests with new wisdom pieces
                            </div>
                        </div>
                        <div class="flex items-start space-x-3">
                            <div class="text-green-500 text-xl">✅</div>
                            <div>
                                <strong>Report Issues:</strong> Help us fix errors or improve accuracy
                            </div>
                        </div>
                        <div class="flex items-start space-x-3">
                            <div class="text-green-500 text-xl">✅</div>
                            <div>
                                <strong>Suggest Sources:</strong> Recommend authentic wisdom texts
                            </div>
                        </div>
                        <div class="flex items-start space-x-3">
                            <div class="text-green-500 text-xl">✅</div>
                            <div>
                                <strong>Translations:</strong> Help translate wisdom into other languages
                            </div>
                        </div>
                    </div>
                    <div class="mt-6">
                        <a href="https://github.com/jnima2022/tibetan-wisdom-api" class="bg-blue-500 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-600 transition inline-flex items-center">
                            <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M10 0C4.477 0 0 4.484 0 10.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0110 4.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.203 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.942.359.31.678.921.678 1.856 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0020 10.017C20 4.484 15.522 0 10 0z" clip-rule="evenodd"></path>
                            </svg>
                            Contribute on GitHub
                        </a>
                    </div>
                </div>
            </div>
        </div>

        <!-- Footer -->
        <footer class="gradient-bg text-white py-8">
            <div class="container mx-auto px-6 text-center">
                <p>&copy; 2025 Tibetan Wisdom API. Built with FastAPI & ❤️ by <strong>Thukpa Labs</strong></p>
                <div class="mt-4">
                    <a href="/docs" class="text-purple-200 hover:text-white mx-4">API Documentation</a>
                    <a href="https://github.com/jnima2022/tibetan-wisdom-api" class="text-purple-200 hover:text-white mx-4">GitHub</a>
                    <a href="mailto:contact@thukpalabs.com" class="text-purple-200 hover:text-white mx-4">Contact Thukpa Labs</a>
                </div>
            </div>
        </footer>

        <script>
            async function getRandomWisdom() {
                try {
                    const response = await fetch('/wisdom/random');
                    const data = await response.json();
                    const wisdom = data.wisdom;
                    
                    document.getElementById('wisdom-text').textContent = `"${wisdom.text}"`;
                    document.getElementById('wisdom-author').textContent = `— ${wisdom.author}`;
                    document.getElementById('wisdom-meta').textContent = `${wisdom.source} | Category: ${wisdom.category}`;
                    document.getElementById('wisdom-display').classList.remove('hidden');
                    
                    // Scroll to wisdom
                    document.getElementById('wisdom-display').scrollIntoView({ behavior: 'smooth' });
                } catch (error) {
                    console.error('Error fetching wisdom:', error);
                }
            }
        </script>
    </body>
    </html>
    """
    return html_content

@app.get("/info", response_model=ApiInfo)
@limiter.limit("10/minute")
async def get_api_info(request: Request):
    """Get API information and statistics"""
    return ApiInfo(
        name="Tibetan Wisdom API",
        version="1.0.0",
        description="Access over 1000 pieces of Tibetan wisdom from Buddhist masters and traditional teachings. Developed by Thukpa Labs.",
        total_wisdom=len(wisdom_data),
        categories=categories,
        authors=authors
    )

@app.get("/wisdom/random", response_model=WisdomResponse)
@limiter.limit("30/minute")
async def get_random_wisdom(request: Request):
    """Get a random piece of wisdom from the collection"""
    if not wisdom_data:
        raise HTTPException(status_code=404, detail="No wisdom available")
    
    random_wisdom = random.choice(wisdom_data)
    return WisdomResponse(wisdom=Wisdom(**random_wisdom))

@app.get("/wisdom", response_model=WisdomListResponse)
@limiter.limit("20/minute")
async def get_wisdom(
    request: Request,
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Wisdom pieces per page"),
    category: Optional[str] = Query(None, description="Filter by category"),
    author: Optional[str] = Query(None, description="Filter by author"),
    source: Optional[str] = Query(None, description="Filter by source")
):
    """Get paginated wisdom with optional filtering"""
    filtered_wisdom = wisdom_data.copy()
    
    # Apply filters
    if category:
        filtered_wisdom = [w for w in filtered_wisdom if w["category"].lower() == category.lower()]
    
    if author:
        filtered_wisdom = [w for w in filtered_wisdom if author.lower() in w["author"].lower()]
    
    if source:
        filtered_wisdom = [w for w in filtered_wisdom if source.lower() in w["source"].lower()]
    
    # Pagination
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_wisdom = filtered_wisdom[start_idx:end_idx]
    
    return WisdomListResponse(
        wisdom=[Wisdom(**w) for w in paginated_wisdom],
        total=len(filtered_wisdom),
        page=page,
        per_page=per_page
    )

@app.get("/wisdom/search", response_model=WisdomListResponse)
@limiter.limit("15/minute")
async def search_wisdom(
    request: Request,
    q: str = Query(..., description="Search query"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=50, description="Wisdom pieces per page")
):
    """Search wisdom by keyword in text, author, or source"""
    search_term = q.lower()
    
    filtered_wisdom = [
        wisdom for wisdom in wisdom_data
        if search_term in wisdom["text"].lower() 
        or search_term in wisdom["author"].lower()
        or search_term in wisdom["source"].lower()
    ]
    
    # Pagination
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_wisdom = filtered_wisdom[start_idx:end_idx]
    
    return WisdomListResponse(
        wisdom=[Wisdom(**w) for w in paginated_wisdom],
        total=len(filtered_wisdom),
        page=page,
        per_page=per_page
    )

@app.get("/wisdom/categories")
@limiter.limit("10/minute")
async def get_categories(request: Request):
    """Get all available categories"""
    return {"categories": sorted(categories)}

@app.get("/wisdom/authors")
@limiter.limit("10/minute")
async def get_authors(request: Request):
    """Get all available authors"""
    return {"authors": sorted(authors)}

@app.get("/wisdom/sources")
@limiter.limit("10/minute")
async def get_sources(request: Request):
    """Get all available sources"""
    return {"sources": sorted(sources)}

@app.get("/wisdom/{wisdom_id}", response_model=WisdomResponse)
@limiter.limit("30/minute")
async def get_wisdom_by_id(request: Request, wisdom_id: int):
    """Get a specific piece of wisdom by ID"""
    wisdom = next((w for w in wisdom_data if w["id"] == wisdom_id), None)
    
    if not wisdom:
        raise HTTPException(status_code=404, detail="Wisdom not found")
    
    return WisdomResponse(wisdom=Wisdom(**wisdom))

@app.get("/health")
@limiter.limit("5/minute")
async def health_check(request: Request):
    """Health check endpoint with basic API statistics"""
    return {
        "status": "healthy",
        "api_version": "1.0.0",
        "total_wisdom": len(wisdom_data),
        "available_categories": len(categories),
        "available_authors": len(authors),
        "rate_limits": {
            "random_wisdom": "30/minute",
            "wisdom_listings": "20/minute", 
            "search": "15/minute",
            "metadata": "10/minute"
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)