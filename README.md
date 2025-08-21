# Tibetan Wisdom API 🧘‍♂️

*Developed by **Thukpa Labs***

A FastAPI-powered REST API serving over 1000 authentic pieces of Tibetan wisdom from the Dalai Lama, Buddhist masters, and traditional teachings.

## 🌟 Features

- **1000+ Wisdom Pieces** from renowned Tibetan Buddhist masters
- **Smart Filtering** by category, author, source
- **Search Functionality** across all wisdom content
- **Random Wisdom Endpoint** for daily inspiration
- **Rate Limiting** to ensure fair usage and optimal performance
- **Beautiful Landing Page** with interactive demo and use cases
- **Auto-Generated Documentation** via FastAPI
- **Fast & Reliable** JSON-based storage
- **Health Monitoring** endpoint for API status
- **Community Contributions** welcome via GitHub

## 📚 Wisdom Sources

- **Dalai Lama XIV** - Contemporary teachings and wisdom
- **Traditional Tibetan Proverbs** - Ancient folk wisdom
- **Buddhist Texts** - Dhammapada, Tibetan Book of the Dead
- **Sogyal Rinpoche** - Tibetan Book of Living and Dying
- **Sakya Pandita** - Classical Tibetan literature
- And many more renowned masters...

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/jnima2022/tibetan-wisdom-api.git
cd tibetan-wisdom-api
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Add wisdom data**
   - Place `tibetan_quotes_collection.json` file in the root directory
   - The file should follow this structure:
```json
{
  "tibetan_quotes_collection": {
    "metadata": {
      "total_quotes": 1000,
      "categories": ["wisdom", "compassion", "..."],
      "sources": ["Dalai Lama XIV", "..."]
    },
    "quotes": [
      {
        "id": 1,
        "text": "Be kind whenever possible. It is always possible.",
        "author": "Dalai Lama XIV",
        "source": "Contemporary Teachings",
        "category": "compassion",
        "language": "English"
      }
    ]
  }
}
```

5. **Run the server**
```bash
python main.py
```

The API will be available at:
- **Main site**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative docs**: http://localhost:8000/redoc

## 🔗 API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Beautiful landing page with demo |
| `GET` | `/wisdom/random` | Get a random piece of wisdom |
| `GET` | `/wisdom` | Get paginated wisdom with filters |
| `GET` | `/wisdom/search` | Search wisdom by keyword |
| `GET` | `/wisdom/{id}` | Get specific wisdom by ID |
| `GET` | `/health` | API health check and statistics |

### Utility Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/wisdom/categories` | List all categories |
| `GET` | `/wisdom/authors` | List all authors |
| `GET` | `/wisdom/sources` | List all sources |
| `GET` | `/info` | API information and stats |

## 🚦 Rate Limits

To ensure fair usage and optimal performance, the API implements the following rate limits per IP address:

| Endpoint Type | Rate Limit | Description |
|---------------|------------|-------------|
| Random wisdom (`/wisdom/random`) | 30/minute | Most popular endpoint |
| Wisdom listings (`/wisdom`) | 20/minute | Paginated data access |
| Search (`/wisdom/search`) | 15/minute | Resource-intensive queries |
| Metadata endpoints | 10/minute | Categories, authors, sources |
| Landing page | 30/minute | Website access |
| Health check | 5/minute | Monitoring endpoint |

**Rate limit exceeded?** You'll receive a `429` status code with retry information.

## 📖 Usage Examples

### Get Random Wisdom
```bash
curl https://tibetan-wisdom-api.onrender.com/wisdom/random
```

### Search for Wisdom by Category
```bash
curl "https://tibetan-wisdom-api.onrender.com/wisdom?category=wisdom&page=1&per_page=5"
```

### Search by Keyword
```bash
curl "https://tibetan-wisdom-api.onrender.com/wisdom/search?q=compassion"
```

### Filter by Author
```bash
curl "https://tibetan-wisdom-api.onrender.com/wisdom?author=Dalai%20Lama"
```

## 💡 Use Cases & Applications

### Mobile & Web Development
- **Daily Inspiration Apps**: Send random wisdom notifications
- **Website Headers**: Display rotating wisdom quotes
- **Email Signatures**: Add meaningful Buddhist teachings
- **Meditation Apps**: Integrate wisdom into mindfulness sessions

### AI & Automation
- **Chatbots**: Train AI with compassionate, wise responses
- **Content Creation**: Generate inspirational content for blogs/social media
- **Educational Platforms**: Enhance learning with profound teachings

### Personal Projects
- **Developer Portfolios**: Showcase API integration skills
- **Spiritual Websites**: Add authentic Tibetan wisdom content
- **Learning Tools**: Create flashcards or study aids with Buddhist teachings

## 🤝 Contributing

We welcome contributions to expand our wisdom collection! You can help by:

### Ways to Contribute
- **Submit Wisdom**: Add authentic Tibetan teachings via GitHub
- **Report Issues**: Help improve accuracy and fix errors  
- **Suggest Sources**: Recommend authentic Buddhist texts
- **Translations**: Help translate wisdom into other languages

### Contribution Guidelines
1. **Fork the repository** on GitHub
2. **Add Quotes/Wisdom** following our JSON format
3. **Verify authenticity** of sources and attributions
4. **Submit a pull request** with clear descriptions

**GitHub Repository**: `https://github.com/jnima2022/tibetan-wisdom-api`

*We review all contributions to maintain authenticity and respect for Tibetan Buddhist tradition.*

## 🚀 Deployment
This API is already live at https://tibetan-wisdom-api.onrender.com, but you can deploy your own instance:

### Deploy to Render

1. **Connect your GitHub repository** to Render
2. **Create a new Web Service**
3. **Configure the service:**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Environment**: Python 3
4. **Deploy!**

### Deploy to PythonAnywhere

1. **Upload your files** to PythonAnywhere
2. **Create a virtual environment**
3. **Install dependencies**: `pip install -r requirements.txt`
4. **Configure WSGI file**:
```python
from main import app
application = app
```

### Environment Variables (Optional)

For production, you might want to set:
```bash
export HOST=0.0.0.0
export PORT=8000
export ENV=production
```

## 🧪 Testing

Test the API endpoints:

```bash
# Test random wisdom
curl http://localhost:8000/wisdom/random

# Test search
curl "http://localhost:8000/wisdom/search?q=happiness"

# Test categories
curl http://localhost:8000/wisdom/categories
```

## 📊 Project Structure

```
tibetan-wisdom-api/
├── main.py                          # FastAPI application
├── requirements.txt                 # Python dependencies
├── tibetan_quotes_collection.json   # Wisdom data
├── README.md                        # This file
└── .gitignore                       # Git ignore file
```

## 🎯 What This Project Demonstrates

### Technical Skills
- **FastAPI** - Modern Python web framework
- **REST API Design** - Clean, intuitive endpoints
- **Rate Limiting** - Professional API protection and fair usage
- **Pydantic Models** - Data validation and serialization
- **Pagination** - Efficient data handling
- **Search & Filtering** - Complex query functionality
- **CORS** - Cross-origin resource sharing
- **Error Handling** - Custom HTTP responses and status codes
- **Documentation** - Auto-generated API docs

### Software Engineering Practices
- **Clean Code** - Well-organized, readable structure
- **Error Handling** - Proper HTTP status codes
- **Data Modeling** - Structured JSON data
- **User Experience** - Beautiful landing page
- **Performance** - Efficient filtering and pagination

## 🌐 Live Demo

- **Landing Page**: https://tibetan-wisdom-api.onrender.com
- **API Docs**: https://tibetan-wisdom-api.onrender.com/docs
- **Random Wisdom**: https://tibetan-wisdom-api.onrender.com/wisdom/random

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Contact & Support

- **Developer**: Thukpa Labs by Jamyang Nima
- **GitHub**: [https://github.com/jnima2022](https://github.com/jnima2022)
- **API Repository**: [https://github.com/jnima2022/tibetan-wisdom-api](https://github.com/jnima2022/tibetan-wisdom-api)
- **Email**: thukpalabs.help@gmail.com

## 🙏 Acknowledgments

Special thanks to:
- The Dalai Lama XIV for his timeless teachings
- Traditional Tibetan Buddhist masters and scholars
- The preservation of authentic Buddhist wisdom through centuries
- Our community contributors who help expand this collection

---

*"Be kind whenever possible. It is always possible." - Dalai Lama XIV*

**Built with ❤️ by Thukpa Labs**