# Daily Read Agent

A lightweight, self-hosted AI agent that automatically selects and delivers **one high-quality article every day** based on your interests.

Instead of manually checking newsletters, blogs, and publications, Daily Read Agent collects recent articles from curated sources, filters previously recommended content, uses an LLM to select the most valuable article, and delivers it directly to your email.

The project was built primarily as a hands-on exploration of **AI system design**, focusing on where AI adds value and where deterministic application logic is more appropriate.

---

## Features

- Personalized interests configured through environment variables
- Curated publication registry for trusted content sources
- Automatic publication setup and RSS validation
- RSS-based article ingestion
- Multi-source article aggregation
- Duplicate and previously recommended article filtering
- Freshness-based candidate filtering
- LLM-based article ranking
- Structured LLM output using Pydantic
- Local LLM support through Ollama
- Optional Groq provider support
- Automated daily scheduling
- Email delivery
- Recommendation history using SQLite
- Failure isolation for unavailable RSS sources
- Provider abstractions for future content sources and LLMs
- Fully local/self-hosted workflow

---

## How It Works

```text
Developer Configuration (.env)
          │
          ▼
      Interests
          │
          ▼
   Preference Sync
          │
          ▼
 Curated Source Registry
          │
          ▼
 Validate RSS Sources
          │
          ▼
 Store Publications
          │
          ▼
      APScheduler
          │
          ▼
   Select Daily Genre
          │
          ▼
 Collect Recent Articles
          │
          ▼
   Candidate Filtering
          │
          ▼
      LLM Ranking
          │
          ▼
   Selected Article
          │
          ▼
     Email Delivery
          │
          ▼
 Recommendation History
          │
          ▼
        SQLite
```

The article is added to recommendation history **only after successful email delivery**, preventing undelivered articles from being incorrectly treated as previously recommended.

---

## Architecture

Daily Read Agent intentionally separates deterministic application logic from LLM-based decisions.

### Deterministic Components

Python and SQL handle operations where the correct behavior is known:

- RSS ingestion
- Duplicate detection
- Publication validation
- Article freshness filtering
- Recommendation-history checks
- Genre eligibility
- Scheduling
- Email delivery
- Persistence

### LLM Components

The LLM is used where subjective judgment is valuable:

- Evaluating article relevance
- Comparing learning value
- Considering technical depth
- Selecting the most useful article
- Generating a concise reason for the recommendation

This avoids using an LLM for operations that can be handled more reliably and cheaply with deterministic code.

---

## Recommendation Pipeline

For each scheduled run:

```text
Choose Genre
     │
     ▼
Find Active Publications
     │
     ▼
Fetch RSS Feeds
     │
     ▼
Aggregate Articles
     │
     ▼
Remove Invalid / Duplicate / Old Articles
     │
     ▼
Remove Previously Recommended Articles
     │
     ▼
Limit Candidate Set
     │
     ▼
LLM Evaluates Candidates
     │
     ▼
Select One Article
     │
     ▼
Send Email
     │
     ▼
Save Successful Recommendation
```

The LLM returns a structured `selected_index` rather than generating the selected article URL itself. Python then resolves that index against the authoritative candidate list.

This reduces the possibility of hallucinated article metadata or URLs.

---

## Curated Source Registry

Users only configure their interests.

For example:

```env
INTERESTS=System Design,AI Engineering
```

Daily Read Agent automatically maps supported interests to curated publications.

Example:

```text
System Design
├── ByteByteGo
├── System Design Newsletter
├── System Design Nuggets
└── Hands On System Design

AI Engineering
├── Latent Space
├── Ahead of AI
├── Interconnects
└── Import AI
```

Before storing a publication, its RSS feed is validated to ensure articles can actually be retrieved.

### Unsupported Interests

If an interest does not currently exist in the curated registry, the application safely skips it and logs a warning.

For example:

```env
INTERESTS=System Design,Kafka
```

may produce:

```text
No curated publications available for interest='Kafka'.
This interest will be skipped.
```

The supported-interest registry can easily be extended with additional publications.

Dynamic source discovery can be added in the future for interests that are not available in the curated registry.

---

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python |
| API | FastAPI |
| Agent Workflow | LangGraph |
| Local LLM | Ollama |
| Default Model | Qwen3 8B |
| LLM Integration | LangChain |
| Database | SQLite |
| ORM | SQLAlchemy |
| Validation | Pydantic |
| RSS Parsing | feedparser |
| Scheduler | APScheduler |
| Delivery | SMTP / Email |

---

## Project Structure

```text
daily-read-agent/
│
├── app/
│   ├── agent/
│   │   ├── graph.py
│   │   └── state.py
│   │
│   ├── api/
│   │   ├── articles.py
│   │   ├── publications.py
│   │   ├── recommendations.py
│   │   └── setup.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   │
│   ├── delivery/
│   │   ├── base.py
│   │   └── email.py
│   │
│   ├── jobs/
│   │   └── daily_read.py
│   │
│   ├── llm/
│   │   └── provider.py
│   │
│   ├── models/
│   │   ├── preference.py
│   │   ├── publication.py
│   │   └── recommendation.py
│   │
│   ├── schemas/
│   │   ├── article.py
│   │   ├── publication.py
│   │   └── ranking.py
│   │
│   ├── services/
│   │   ├── article_collector.py
│   │   ├── article_ranker.py
│   │   ├── candidate_filter.py
│   │   ├── candidate_service.py
│   │   ├── genre_selector.py
│   │   ├── preference_setup.py
│   │   ├── publication_setup.py
│   │   ├── recommendation_history.py
│   │   └── recommendation_service.py
│   │
│   ├── sources/
│   │   ├── base.py
│   │   ├── factory.py
│   │   ├── registry.py
│   │   └── substack.py
│   │
│   ├── main.py
│   └── scheduler.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd daily-read-agent
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it.

macOS/Linux:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Ollama

Install Ollama and download the default model:

```bash
ollama pull qwen3:8b
```

Make sure Ollama is running before generating recommendations.

---

## Environment Configuration

Copy the example environment file:

```bash
cp .env.example .env
```

Configure:

```env
LLM_PROVIDER=ollama
LLM_MODEL=qwen3:8b
GROQ_API_KEY=

INTERESTS=System Design,AI Engineering

EMAIL_SENDER=your-email@gmail.com
EMAIL_PASSWORD=your-gmail-app-password
EMAIL_RECIPIENT=your-email@gmail.com

SCHEDULER_TIMEZONE=Asia/Kolkata
DAILY_READ_HOUR=8
DAILY_READ_MINUTE=0
```

### Interests

Interests are comma-separated:

```env
INTERESTS=System Design,AI Engineering
```

On application startup, Daily Read Agent:

1. Reads the configured interests.
2. Synchronizes them with SQLite.
3. Finds matching sources in the curated registry.
4. Validates their RSS feeds.
5. Stores valid publications.

No manual publication configuration is required for supported interests.

---

## Gmail Setup

For Gmail delivery, use a **Google App Password** rather than your normal Gmail password.

Configure:

```env
EMAIL_SENDER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
EMAIL_RECIPIENT=destination@gmail.com
```

The sender and recipient may be the same account.

---

## Run the Application

Start FastAPI:

```bash
uvicorn app.main:app --reload
```

The application will:

```text
Sync Interests
      ↓
Configure Publications
      ↓
Validate Sources
      ↓
Start Daily Scheduler
```

The scheduler then runs at the configured time.

Example:

```env
SCHEDULER_TIMEZONE=Asia/Kolkata
DAILY_READ_HOUR=8
DAILY_READ_MINUTE=0
```

means the recommendation workflow runs daily at **08:00 Asia/Kolkata**.

The application must be running for the local APScheduler job to execute.

---

## Manual Testing

You can manually trigger the complete daily workflow from Python:

```python
from app.jobs.daily_read import run_daily_read

run_daily_read()
```

This runs:

```text
Genre Selection
      ↓
Article Collection
      ↓
Candidate Filtering
      ↓
LLM Ranking
      ↓
Email Delivery
      ↓
Recommendation History
```

---

## Example Recommendation

```text
☀️ Today's Read

Topic: System Design

Designing Reliable Distributed Systems

Why this was selected:
This article provides a practical explanation of reliability patterns
and demonstrates how they apply to production distributed systems.

Read:
https://example.com/article
```

---

## Content Source Abstraction

Content ingestion is not tightly coupled to a single platform.

Sources implement a common abstraction:

```text
ContentSource
     │
     ├── SubstackSource
     │
     ├── MediumSource       (future)
     │
     └── BlogSource         (future)
```

The current implementation primarily uses RSS-based Substack publications.

This allows additional content providers to be introduced without changing the recommendation pipeline.

---

## LLM Provider Abstraction

The recommendation system is also separated from the underlying LLM provider.

```text
Recommendation Engine
        │
        ▼
    LLM Provider
      /       \
 Ollama       Groq
```

The default configuration uses:

```env
LLM_PROVIDER=ollama
LLM_MODEL=qwen3:8b
```

This keeps the application fully local and free.

The provider abstraction allows cloud-hosted models to be introduced without changing the ranking logic.

---

## Failure Handling

The application is designed so individual failures do not unnecessarily break the entire workflow.

### Broken RSS Source

If one publication becomes unavailable:

```text
Publication A → works
Publication B → broken
Publication C → works
```

the collector skips Publication B and continues processing the remaining sources.

### No Candidates

If no valid candidates exist for a selected genre, the workflow stops without sending an invalid recommendation.

### Email Failure

Recommendation history is updated only **after successful email delivery**.

Therefore:

```text
Select Article
      ↓
Email fails
      ↓
Do NOT save recommendation
```

The article remains eligible for a future attempt.

### Unsupported Interest

Unsupported interests are skipped while supported interests continue working normally.

---

## Design Decisions

### Why RSS?

RSS provides a lightweight and deterministic way to retrieve publication content without scraping websites or depending on paid APIs.

### Why a Curated Registry?

Automatically discovering arbitrary publications introduces search infrastructure, source-quality problems, and additional external dependencies.

For V1, Daily Read Agent deliberately uses curated sources to prioritize:

- Content quality
- Predictable behavior
- Zero-cost operation
- Simple local setup
- Reliable RSS ingestion

### Why SQLite?

The project has modest persistence requirements:

- Preferences
- Publications
- Recommendation history

SQLite keeps the system simple and fully local while still providing proper persistence and SQL querying.

### Why Not a Vector Database?

The candidate set is intentionally reduced before ranking, and the system does not currently require semantic retrieval over a large document corpus.

Adding a vector database would introduce complexity without solving a current requirement.

### Why One Agent?

This workflow does not require multiple autonomous agents.

A single LangGraph workflow is sufficient for orchestrating candidate collection and ranking while deterministic services handle the rest of the system.

---

## Current Limitations

- Curated sources currently support a limited set of interests.
- Arbitrary-interest publication discovery is not implemented.
- RSS availability depends on external publishers.
- APScheduler requires the application process to remain running.
- Email delivery currently uses SMTP.
- The system is designed primarily as a self-hosted single-user application.

---

## Future Improvements

Potential extensions include:

- Dynamic publication discovery for unsupported interests
- Additional curated interest categories
- More RSS/content providers
- Medium and independent-blog adapters
- User feedback signals
- Recommendation scoring improvements
- Multiple delivery providers
- Docker support
- Multi-user support
- Cloud deployment
- Web interface

These are intentionally outside the scope of V1.

---

## What This Project Explores

Daily Read Agent was built as a hands-on AI system design project rather than as an attempt to create an unnecessarily complex recommendation platform.

The project explores:

- Separating deterministic logic from LLM reasoning
- Structured LLM outputs
- Candidate reduction before LLM inference
- Provider abstraction
- Agent workflow orchestration
- External-source failure isolation
- Idempotent setup workflows
- Scheduling AI workflows
- Side-effect ordering and delivery consistency
- Persistent recommendation history
- Designing for local-first AI
- Keeping AI architecture proportional to the problem

A major design principle throughout the project is:

> **Use AI where judgment is required. Use deterministic software where correctness is known.**

---

## License

This project is intended for learning, experimentation, and extension. Add your preferred open-source license before distribution.
