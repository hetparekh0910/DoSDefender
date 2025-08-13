# 🛡️ DoSDefender - DoS Attack Analysis & Education Platform

A comprehensive cybersecurity education tool built with Streamlit that provides analysis, visualization, and learning resources for understanding Denial of Service (DoS) attacks.

## 🌟 Features

- **🔍 Attack Analyzer**: Interactive DoS attack flow analysis and traffic pattern recognition
- **📚 Case Studies**: Real-world attack documentation with detailed analysis
- **🎯 Attack Vectors**: Comprehensive breakdown of DoS attack methodologies
- **💥 Impact Analysis**: System and business impact assessment tools
- **📈 Timeline Visualization**: Attack progression and historical timeline analysis
- **📖 Educational Resources**: Learning modules, quizzes, and reference materials
- **🗄️ Database Admin**: Management interface for attack data and content

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- PostgreSQL database (or SQLite for development)

### Local Development Setup

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/DoSDefender.git
cd DoSDefender
```

2. **Create virtual environment**
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
# OR
source .venv/bin/activate   # Linux/Mac
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up database**
```bash
# Option 1: PostgreSQL (Production)
$env:DATABASE_URL = "postgresql://username:password@host:port/database"

# Option 2: SQLite (Development)
$env:DATABASE_URL = "sqlite:///dosdefender.db"
```

5. **Run the application**
```bash
streamlit run app.py
```

The app will be available at: http://localhost:8501

## 🗄️ Database Configuration

### PostgreSQL (Recommended for Production)
- **Supabase**: Free tier available
- **Railway**: Free tier available  
- **Neon**: Free tier available
- **Local PostgreSQL**: For development

### Environment Variables
Create a `.env` file in the project root:
```env
DATABASE_URL=postgresql://username:password@host:port/database
```

## 🚀 Deployment

### Streamlit Cloud (Recommended)
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select your repository
5. Deploy!

### Other Options
- **Railway**: Full-stack deployment platform
- **Heroku**: Production-grade hosting
- **Docker**: Containerized deployment

## 📁 Project Structure

```
DoSDefender/
├── app.py                          # Main application entry point
├── components/                     # UI components
│   ├── attack_analyzer.py         # Attack analysis tools
│   ├── case_studies.py            # Case study browser
│   ├── attack_vectors.py          # Attack methodology analysis
│   ├── impact_analysis.py         # Impact assessment
│   ├── timeline_viz.py            # Timeline visualization
│   ├── educational_resources.py   # Learning modules
│   └── database_admin.py          # Database management
├── database/                       # Database layer
│   ├── schema.py                  # SQLAlchemy models
│   └── data_manager.py            # Database operations
├── data/                          # Data layer
│   └── dos_attacks_database.py    # Data access
├── utils/                         # Utility functions
│   └── data_processing.py         # Data processing utilities
├── requirements.txt                # Python dependencies
├── .gitignore                     # Git ignore rules
└── README.md                      # This file
```

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python, SQLAlchemy
- **Database**: PostgreSQL/SQLite
- **Visualization**: Plotly, NetworkX
- **Data Processing**: Pandas, NumPy

## 📚 Educational Purpose

⚠️ **This tool is designed exclusively for educational and defensive purposes.**

- Cybersecurity education
- Defensive strategy development
- Understanding attack patterns
- Security awareness training

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues:
1. Check the [Issues](https://github.com/YOUR_USERNAME/DoSDefender/issues) page
2. Create a new issue with detailed information
3. Include your environment details and error messages

## 🙏 Acknowledgments

- Built with Streamlit
- Data visualization powered by Plotly
- Network analysis with NetworkX
- Database operations with SQLAlchemy

---

**Made with ❤️ for cybersecurity education**
