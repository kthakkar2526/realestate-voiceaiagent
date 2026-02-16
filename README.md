# PropertyAI - Real Estate AI Assistant

An AI-powered real estate platform that uses voice and chat agents to help customers find properties, manage preferences, and book site visits. Built with Google Gemini 2.0 Flash, FastAPI, and Next.js.

## Features

- **AI Chat Agent** - Natural language property search and booking via text
- **Voice Assistant** - Vapi.ai-powered voice concierge for hands-free interaction
- **Smart Property Search** - Filter by city, location, budget, BHK, property type, and amenities
- **Automated Bookings** - Schedule site visits with email and WhatsApp confirmations
- **OTP Authentication** - Phone-based login with Twilio SMS
- **Lead Tracking** - Automatic lead capture from every conversation
- **Admin Dashboard** - Manage properties, leads, and bookings
- **Background Scheduler** - Automated booking reminders and inactive lead follow-ups
- **LLM Observability** - Langfuse integration for monitoring AI conversations

## Tech Stack

**Backend:** Python, FastAPI, SQLAlchemy, PostgreSQL, Google Gemini 2.0 Flash

**Frontend:** Next.js 16, React 19, TypeScript, Tailwind CSS 4

**Integrations:** Vapi.ai (Voice), Twilio (SMS/WhatsApp), Langfuse, APScheduler

## Project Structure

```
├── backend/
│   └── app/
│       ├── main.py              # FastAPI entry point
│       ├── models.py            # SQLAlchemy models
│       ├── schemas.py           # Pydantic schemas
│       ├── config.py            # Environment configuration
│       ├── notifications.py     # Email & WhatsApp sending
│       ├── scheduler.py         # Background jobs
│       ├── agent/
│       │   ├── engine.py        # Gemini AI agent
│       │   ├── tools.py         # Tool declarations & execution
│       │   ├── prompts.py       # System prompt
│       │   └── session.py       # Conversation sessions
│       └── routers/
│           ├── auth.py          # OTP & JWT auth
│           ├── chat.py          # Chat endpoint
│           ├── properties.py    # Property CRUD
│           ├── bookings.py      # Booking management
│           ├── leads.py         # Lead tracking
│           └── vapi_webhook.py  # Voice webhook
├── frontend/
│   └── src/
│       ├── app/                 # Next.js pages
│       ├── components/          # Chat, Voice, UI components
│       ├── lib/                 # API client & auth context
│       └── types/               # TypeScript types
└── requirements.txt
```

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL

### Backend Setup

1. Install dependencies:
   ```bash
   cd backend
   pip install -r ../requirements.txt
   ```

2. Create a `.env` file in the backend directory:
   ```env
   GEMINI_API_KEY=your_gemini_api_key
   DATABASE_URL=postgresql://user:password@localhost:5432/realestate
   JWT_SECRET=your_jwt_secret

   # Twilio (SMS & WhatsApp)
   TWILIO_ACCOUNT_SID=your_sid
   TWILIO_AUTH_TOKEN=your_token
   TWILIO_PHONE_NUMBER=your_number

   # Email
   SMTP_EMAIL=your_email@gmail.com
   SMTP_PASSWORD=your_app_password

   # Langfuse (optional)
   LANGFUSE_PUBLIC_KEY=your_key
   LANGFUSE_SECRET_KEY=your_secret
   LANGFUSE_HOST=https://cloud.langfuse.com

   # Vapi (optional)
   VAPI_API_KEY=your_key
   VAPI_PUBLIC_KEY=your_key
   PUBLIC_URL=http://localhost:8000
   ```

3. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Run the dev server:
   ```bash
   npm run dev
   ```

The app will be available at `http://localhost:3000`.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/send-otp` | Send OTP to phone |
| POST | `/api/auth/verify-otp` | Verify OTP, get JWT |
| GET | `/api/auth/me` | Get current user |
| POST | `/api/chat` | Send chat message |
| POST | `/api/vapi/webhook` | Vapi voice webhook |
| GET | `/api/properties` | List properties |
| GET | `/api/properties/{id}` | Get property details |
| POST | `/api/properties` | Create property (admin) |
| GET | `/api/bookings` | List bookings |
| GET | `/api/leads` | List leads (admin) |
| GET | `/api/health` | Health check |

## How It Works

1. **User starts a conversation** via chat or voice
2. **AI agent gathers preferences** - budget, city, property type, BHK
3. **Agent searches properties** using function calling tools
4. **User browses results** and selects properties of interest
5. **Agent books a site visit** and sends confirmation via email/WhatsApp
6. **Scheduler sends reminders** 1 day before the visit

## AI Agent Tools

| Tool | Description |
|------|-------------|
| `search_properties` | Search by city, location, type, budget, BHK, amenities |
| `save_requirements` | Store user preferences |
| `book_visit` | Schedule a property visit |
| `save_contact` | Save lead contact info |
| `get_property_details` | Fetch full property details |

## License

MIT
