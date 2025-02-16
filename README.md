# AI Capstone Project: Revenue Prediction System

This project implements a production-ready revenue prediction system using time series analysis and machine learning.

## Project Structure

```
├── app/
│   ├── api/          # FastAPI application
│   ├── models/       # Trained models
│   ├── data/         # Data storage
│   ├── utils/        # Utilities (logging, monitoring)
│   └── tests/        # Test suites
├── notebooks/        # Jupyter notebooks for analysis
├── docker/          # Docker configuration
└── scripts/         # Utility scripts
```

## Features

- FastAPI-based REST API with health checks and metrics
- Automated data ingestion pipeline
- Real-time monitoring and logging
- Containerized deployment with Docker
- Comprehensive test suite
- Country-specific revenue predictions

## Getting Started

### Prerequisites

- Python 3.9+
- Docker
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/AI-capstone-project.git
cd AI-capstone-project
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

1. Start the API:
```bash
uvicorn app.api.main:app --reload
```

2. Run with Docker:
```bash
cd docker
docker build -t revenue-predictor .
docker run -p 8000:8000 revenue-predictor
```

### Running Tests

```bash
./run_all_tests.sh
```

## API Endpoints

- `GET /health`: Health check endpoint
- `GET /predict/{country}`: Get revenue prediction for specific country
- `GET /predict/all`: Get predictions for all countries
- `GET /metrics`: Get model performance metrics

## Development

### Data Pipeline

The data ingestion pipeline (`scripts/data_ingestion.py`) handles:
- Data fetching from sources
- Data cleaning and preprocessing
- Feature engineering
- Data storage

### Monitoring

The system includes:
- Performance monitoring
- API request logging
- Model prediction tracking
- Error monitoring

### Testing

Tests cover:
- API endpoints
- Model performance
- Data pipeline
- Logging system

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/NewFeature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/NewFeature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
