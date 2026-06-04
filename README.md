# ☀️ Solar Plant IoT Monitoring & Fault Detection

End-to-end IoT pipeline — real inverter telemetry → AWS cloud → ML anomaly detection → live alerts & dashboard

![Python](https://img.shields.io/badge/Python-3.12-blue)
![AWS](https://img.shields.io/badge/AWS-IoT%20Core-orange)
![ML](https://img.shields.io/badge/ML-Isolation%20Forest-green)
![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-red)

## 🎯 Goal
Build a system that takes real inverter telemetry, pushes it through an AWS IoT pipeline, detects faults automatically using ML, sends email alerts when something is wrong, and displays everything on a live dashboard.

## 🏗️ Architecture

Growatt CSV → MQTT (paho) → AWS IoT Core → DynamoDB
                                    ↓
                              IoT Rule triggers
                            ↙              ↘
                      DynamoDB          Lambda
                   (stores all)    (checks anomaly)
                                         ↓
                                   SNS Email Alert

## 📊 Results
- **36,823** daytime inverter readings processed
- **1,842 faults detected** (5%) using Isolation Forest
- Real-time email alerts triggered on every fault
- Live Streamlit dashboard with power charts and fault table

## 🔧 Tech Stack
| Layer | Technology |
|-------|-----------|
| Data | Kaggle Solar Dataset + Real Growatt Telemetry |
| IoT | MQTT (paho), AWS IoT Core |
| Cloud | AWS DynamoDB, Lambda, SNS |
| ML | Isolation Forest (scikit-learn) |
| Dashboard | Streamlit |
| Language | Python 3.12 |

## 🚀 How to Run

### 1. Clone the repo
git clone https://github.com/udaykirank23-bli/solar_iot_monitot.git
cd solar_iot_monitot

### 2. Install dependencies
pip install -r requirements.txt

### 3. Add your AWS certificates
Place your AWS IoT certificates in src/certs/:
- certificate.pem.crt
- private.pem.key
- AmazonRootCA1.pem

### 4. Run the MQTT publisher
python src/mqtt_publisher.py

### 5. Launch the dashboard
streamlit run dashboard/dashboard.py

## 📁 Project Structure
solar-iot-monitor/
├── data/               # Raw + processed CSVs (not tracked)
├── notebooks/          # EDA + feature engineering
├── src/
│   ├── mqtt_publisher.py   # Publishes telemetry to AWS IoT
│   └── certs/              # AWS certificates (not tracked)
├── dashboard/
│   └── dashboard.py        # Streamlit live dashboard
└── requirements.txt

## 👤 Author
**Uday Kiran Kummari**
ECE, IIIT Sricity | [LinkedIn](https://linkedin.com/in/uday-kiran-kummari-4924083bb) | [GitHub](https://github.com/udaykirank23-bli)