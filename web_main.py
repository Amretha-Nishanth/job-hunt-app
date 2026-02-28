import os
import json
from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS
from dotenv import load_dotenv
import requests as http_requests

load_dotenv()

# Templates at root level - most reliable on Render
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, 
            template_folder=BASE_DIR,
            static_folder=os.path.join(BASE_DIR, 'static'))
CORS(app)

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

def get_supabase():
    if not SUPABASE_URL or not SUPABASE_KEY:
        return None
    try:
        from supabase import create_client
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception:
        return None

def call_claude(prompt):
    if not ANTHROPIC_API_KEY:
        return "Error: ANTHROPIC_API_KEY not set. Add it in Render → Environment Variables."
    try:
        res = http_requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            json={
                "model": "claude-haiku-4-5-20251001",
                "max_tokens": 2048,
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=60
        )
        data = res.json()
        if "error" in data:
            return f"API error: {data['error']['message']}"
        return data["content"][0]["text"]
    except Exception as e:
        return f"Error: {str(e)}"

PROFILE = {
    "name": "Amretha Karthikeyan",
    "address": "#02-321 153 Gangsa Road, Singapore-670153",
    "mobile": "+65-90256503",
    "email": "amretha.ammu@gmail.com",
    "linkedin": "https://www.linkedin.com/in/amretha-nishanth-534b39101/",
    "headline": "Product Owner | Lead BA | Fintech & Digital Products · Singapore",
    "aiProjectUrl": "https://stock-monitor-8ak6.onrender.com",
    "summary": (
        "SAFe 6.0 certified Product Owner and Lead Business Analyst with 5+ years owning "
        "product backlogs and driving digital product delivery in fintech and banking. "
        "At KPMG Singapore, served as de-facto Product Owner for Loan IQ — a core banking "
        "platform — leading cross-functional squads (engineering, UX, QA) to ship features "
        "and deliver measurable business outcomes. Built and deployed a live AI-powered Trade "
        "Analysis platform using Claude Opus 4.6. Seeking in-house product roles to own "
        "roadmaps end-to-end, from discovery through to scale."
    ),
    "skills": [
        "Tableau", "Power BI", "PSQL", "Python", "Agile", "JIRA", "Excel",
        "Microsoft Project", "Product Vision", "Roadmapping", "Business Analysis",
        "Risk Mitigation", "Change Management", "Budget Forecasting", "Variance Analysis",
        "KPI Tracking", "Dashboard Reporting", "SAFe 6.0", "API integrations",
        "Loan IQ", "SQL", "Stakeholder Management", "Generative AI", "LLM",
        "Claude API", "AI product development", "Prompt Engineering"
    ],
    "certification": "Scaled Agile Framework 6.0 Product Owner/Product Management",
    "experience": [
        {
            "company": "KPMG, Singapore",
            "role": "Lead Business Analyst – Functional Consultant – Loan IQ",
            "period": "Feb 2021 – Present",
            "bullets": [
                "Served as de-facto Product Owner for Loan IQ core banking platform, owning the product backlog and driving sprint delivery for a cross-functional squad (engineering, UX, QA)",
                "Partnered with Enterprise Singapore on large-scale digital transformation projects",
                "Drove product scope decisions through impact analysis, generating ~5% additional business value",
                "Identified and delivered automation of interest computation workflow, eliminating 30 man-days of manual effort",
                "Owned and prioritised product backlog, ensuring alignment with business objectives and regulatory requirements",
                "Led sprint ceremonies (planning, reviews, retros, PI Planning) across multi-squad programme",
                "Managed 3rd party vendors, conducted go-live planning, and led data migrations from legacy systems",
                "Designed and executed end-to-end test scenarios on Loan IQ applications (M&A, Trade, WCL, FA)"
            ],
            "achievements": [
                "Drove ~5% business value through product scope and change request impact analysis",
                "Eliminated 30 man-days of manual work through automated interest computation feature",
                "Led team through critical sprint-to-SIT transition, maintaining delivery timeline"
            ]
        },
        {
            "company": "J.P. Morgan",
            "role": "Asset Management Virtual Internship",
            "period": "Oct 2023 – Jan 2024",
            "bullets": [
                "Gathered product requirements from trading/execution teams to build robust investor profiles",
                "Performed quantitative analysis of 5 stocks and recommended to 2 clients based on risk metrics",
                "Measured portfolio performance via KPIs: Annual Return, Portfolio Variance, Standard Deviation"
            ]
        },
        {
            "company": "Amazon Inc, India",
            "role": "Business Analyst",
            "period": "Mar 2018 – Mar 2019",
            "bullets": [
                "Built real-time quality monitoring dashboards using Power BI from SQL Server and MS Excel",
                "Translated business requirements into functional and non-functional specifications",
                "Analysed and visualised operational data using Tableau and Power BI"
            ]
        }
    ],
    "education": [
        {"degree": "Master of Science – Engineering Business Management", "school": "Coventry University, UK", "period": "Jul 2019 – Nov 2020"},
        {"degree": "Bachelor of Engineering – Electronics & Communication", "school": "Anna University, India", "period": "Jul 2012 – Jun 2016"}
    ],
    "projects": [
        {
            "title": "AI-Powered Trade Analysis Platform",
            "type": "Personal Project",
            "period": "2025",
            "url": "https://stock-monitor-8ak6.onrender.com",
            "tech": "Claude Opus 4.6 (Anthropic), Python, Flask, Render",
            "bullets": [
                "Designed and deployed a live AI-powered Trade Analysis platform using Claude Opus 4.6 — accessible at https://stock-monitor-8ak6.onrender.com",
                "Combined financial trade data and international trade flow analysis using generative AI",
                "Demonstrated end-to-end AI product development: problem definition, prompt engineering, LLM integration, Flask backend, and Render deployment",
                "Independently shipped a working AI product — demonstrating product ownership beyond theory"
            ]
        }
    ]
}

PRODUCT_FRAMING = """
CRITICAL POSITIONING — She is transitioning from CONSULTING to IN-HOUSE PRODUCT roles:
- Reframe "KPMG consultant" → "Product Owner for Loan IQ product squad"
- Reframe "client delivery" → "shipped product features, owned backlog, drove sprint outcomes"
- DO NOT use: consultant, client, engagement, billable, service delivery
- DO USE: product, squad, roadmap, discovery, iteration, user value, outcome, feature, backlog
"""

def is_ai_role(jd, role_type):
    ai_terms = ["ai", "artificial intelligence", "machine learning", "ml", "llm",
                "generative ai", "genai", "nlp", "gpt", "claude", "openai",
                "foundation model", "large language model", "ai product", "data science"]
    text = (jd + " " + role_type).lower()
    return any(t in text for t in ai_terms)


# ─── ROUTES ───────────────────────────────────────────────

@app.route("/", methods=["GET", "HEAD"])
@app.route("/index.html")
def index():
    try:
        return render_template("index.html")
    except Exception as e:
        app.logger.error(f"Template error: {e}")
        return f"<h2>App is running!</h2><p>Template error: {e}</p><p>BASE_DIR: {BASE_DIR}</p>", 500

@app.route("/api/tailor-resume", methods=["POST"])
def tailor_resume():
    data = request.json
    jd = data.get("jd", "")
    role_type = data.get("roleType", "Business Analyst")
    ai_role = is_ai_role(jd, role_type)

    prompt = f"""You are an expert resume writer helping candidates transition into in-house product roles.
{PRODUCT_FRAMING}

Rewrite the following candidate's resume to match the job description. Target role: {role_type}.

CANDIDATE PROFILE:
{json.dumps(PROFILE, indent=2)}

JOB DESCRIPTION:
{jd}

{"AI ROLE DETECTED: Prominently feature the AI Project section with the live URL: " + PROFILE['aiProjectUrl'] + ". Lead Skills with AI/LLM skills." if ai_role else ""}

Write a complete ATS-optimised resume with:
- Header (name, contact, LinkedIn, {PROFILE['aiProjectUrl'] if ai_role else ''})
- Professional Summary (product-ownership framing, keyword-rich)
- {"AI & Innovation / Projects section (FIRST after summary for AI roles)" if ai_role else ""}
- Core Skills
- Professional Experience (product language throughout, real metrics)
- Education & Certifications

Do not fabricate experience. Use product language, not consulting language."""

    result = call_claude(prompt)
    return jsonify({"result": result, "isAiRole": ai_role})

@app.route("/api/cover-letter", methods=["POST"])
def cover_letter():
    data = request.json
    jd = data.get("jd", "")
    role_type = data.get("roleType", "Business Analyst")
    company = data.get("company", "the company")
    ai_role = is_ai_role(jd, role_type)

    prompt = f"""Write a professional 300-350 word cover letter for {PROFILE['name']} applying to {role_type} at {company}.
{PRODUCT_FRAMING}

KEY ACHIEVEMENTS:
- At KPMG: drove ~5% business value through product scope decisions
- At KPMG: eliminated 30 man-days through automation feature
- SAFe 6.0 certified Product Owner/Product Manager
- Personal AI Project: Built and deployed live Trade Analysis platform using Claude Opus 4.6 — {PROFILE['aiProjectUrl']}

JOB DESCRIPTION:
{jd}

{"IMPORTANT — AI ROLE: Mention the live Trade Analysis platform (" + PROFILE['aiProjectUrl'] + ") as hard proof she ships AI products. Include the URL." if ai_role else ""}

Write a compelling cover letter that:
1. Opens with a confident hook about building products, not delivering services
2. Highlights KPMG metrics (5% value, 30 man-days)
3. {"Mentions live AI project with URL as key differentiator" if ai_role else "Bridges consulting delivery to product ownership"}
4. Shows genuine enthusiasm for {company}
5. Ends with clear call to action

Exactly 300-350 words. No consulting jargon. Sound like a product person."""

    result = call_claude(prompt)
    return jsonify({"result": result})

@app.route("/api/interview-prep", methods=["POST"])
def interview_prep():
    data = request.json
    company = data.get("company", "the company")
    role_type = data.get("roleType", "Business Analyst")
    jd = data.get("jd", "")

    prompt = f"""Generate a comprehensive interview prep guide for {PROFILE['name']} interviewing at {company} for {role_type}.
{PRODUCT_FRAMING}

CANDIDATE:
- KPMG Singapore (Feb 2021–Present): De-facto Product Owner for Loan IQ. Drove 5% business value, saved 30 man-days through automation, led sprint-to-SIT delivery
- J.P. Morgan (Oct 2023–Jan 2024): Portfolio KPI analysis, requirement gathering
- Amazon India (Mar 2018–Mar 2019): Power BI dashboards, data products
- SAFe 6.0 certified, Agile, JIRA, SQL, Tableau, Power BI
- Built and deployed live AI Trade Analysis platform: {PROFILE['aiProjectUrl']}
{"JD: " + jd if jd else ""}

Create prep with these EXACT sections:

## 5 Behavioral Questions with STAR Answers
For each: the question, then full STAR answer using her real experience with specific metrics.

## 5 Technical Questions for {role_type}
Questions with model answers specific to this role.

## 3 Things to Research About {company}
Specific actionable research areas.

## 5 Smart Questions to Ask the Interviewer
Product-minded questions that signal ownership thinking.

## Salary Negotiation Tip (Singapore Market)
Specific tip for SAFe-certified PO/BA with 5+ years in Singapore fintech."""

    result = call_claude(prompt)
    return jsonify({"result": result})

@app.route("/api/full-kit", methods=["POST"])
def full_kit():
    data = request.json
    company = data.get("company", "")
    role = data.get("role", "")
    role_type = data.get("roleType", "Business Analyst")
    jd = data.get("jd", "")
    ai_role = is_ai_role(jd, role_type)

    profile_str = json.dumps({k: v for k, v in PROFILE.items()}, indent=2)

    resume_prompt = f"Write ATS-optimised resume for {PROFILE['name']} applying to {role} at {company} ({role_type}). {PRODUCT_FRAMING} Profile: {profile_str}. JD: {jd}. {'AI role: feature project ' + PROFILE['aiProjectUrl'] + ' prominently.' if ai_role else ''}"
    cover_prompt = f"Write 300-word cover letter for {PROFILE['name']} for {role} at {company}. Highlight: 5% KPMG value, 30 man-days saved, SAFe 6.0. {'Mention live AI project: ' + PROFILE['aiProjectUrl'] if ai_role else ''} Product language, no consulting jargon."
    prep_prompt = f"Give top 5 interview questions for {role_type} at {company} with brief model answers for {PROFILE['name']} (KPMG PO, SAFe 6.0, AI project at {PROFILE['aiProjectUrl']}). Be specific."

    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor() as executor:
        r_future = executor.submit(call_claude, resume_prompt)
        c_future = executor.submit(call_claude, cover_prompt)
        p_future = executor.submit(call_claude, prep_prompt)
        resume = r_future.result()
        cover = c_future.result()
        prep = p_future.result()

    return jsonify({"resume": resume, "cover": cover, "prep": prep, "isAiRole": ai_role})

@app.route("/api/follow-up", methods=["POST"])
def follow_up():
    data = request.json
    company = data.get("company", "the company")
    role = data.get("role", "the role")
    days = data.get("days", 7)

    prompt = f"""Write a polite 3-line follow-up email from Amretha Karthikeyan about her application for {role} at {company}, submitted {days} days ago.
Include: subject line, brief message referencing the role, continued interest, offer to provide more info.
Under 80 words. Ready to copy-paste. Professional and confident."""

    result = call_claude(prompt)
    return jsonify({"result": result})

@app.route("/api/speed-kit", methods=["POST"])
def speed_kit():
    data = request.json
    company = data.get("company", "this company")
    role = data.get("role", "this role")

    prompt = f"""Write a genuine 3-sentence "Why do you want to work at {company}?" answer for Amretha Karthikeyan, a SAFe 6.0 PO/Lead BA transitioning from KPMG to an in-house {role} role. Be specific to {company}'s product/market. Sound like a product person who wants to build. No consulting language."""

    result = call_claude(prompt)
    return jsonify({"result": result})


@app.route("/api/generic", methods=["POST"])
def generic():
    data = request.json
    prompt = data.get("prompt", "")
    system = data.get("systemPrompt", "")
    full_prompt = f"{system}\n\n{prompt}" if system else prompt
    result = call_claude(full_prompt)
    return jsonify({"result": result})


@app.route("/api/jobs", methods=["GET"])
def get_jobs():
    """Load all jobs from Supabase."""
    sb = get_supabase()
    if not sb:
        return jsonify({"error": "Supabase not configured", "jobs": []}), 200
    try:
        res = sb.table("jobs").select("*").order("created_at", desc=False).execute()
        return jsonify({"jobs": res.data or []})
    except Exception as e:
        return jsonify({"error": str(e), "jobs": []}), 200


@app.route("/api/jobs/upsert", methods=["POST"])
def upsert_jobs():
    """Save/update jobs to Supabase. Upserts by job id."""
    sb = get_supabase()
    if not sb:
        return jsonify({"error": "Supabase not configured"}), 200
    data = request.json
    jobs = data.get("jobs", [])
    if not jobs:
        return jsonify({"ok": True, "count": 0})
    try:
        # Whitelist all fields we want to persist — everything
        def clean(j):
            return {
                "id":               str(j.get("id", "")),
                "role":             j.get("role", ""),
                "company":          j.get("company", ""),
                "status":           j.get("status", "saved"),
                "url":              j.get("url", ""),
                "linkedInId":       j.get("linkedInId", ""),
                "jd":               (j.get("jd") or "")[:8000],
                "roleType":         j.get("roleType", ""),
                "source":           j.get("source", ""),
                "salary":           j.get("salary", ""),
                "dateApplied":      j.get("dateApplied", ""),
                "aiScore":          j.get("aiScore"),
                "aiLabel":          j.get("aiLabel", ""),
                "aiReason":         j.get("aiReason", ""),
                "aiPriority":       j.get("aiPriority", ""),
                "notes":            j.get("notes", ""),
                "resume_docx_b64":  (j.get("resume_docx_b64") or "")[:500000],
                "cover_docx_b64":   (j.get("cover_docx_b64") or "")[:500000],
                "resume_variant":   j.get("resume_variant", ""),
                "resume_filename":  j.get("resume_filename", ""),
                "cover_filename":   j.get("cover_filename", ""),
                "resume_generated_at": j.get("resume_generated_at", ""),
            }
        cleaned = [clean(j) for j in jobs if j.get("id")]
        res = sb.table("jobs").upsert(cleaned, on_conflict="id").execute()
        return jsonify({"ok": True, "count": len(cleaned)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/jobs/delete", methods=["POST"])
def delete_job():
    """Delete a job from Supabase by id."""
    sb = get_supabase()
    if not sb:
        return jsonify({"error": "Supabase not configured"}), 200
    data = request.json
    job_id = data.get("id")
    if not job_id:
        return jsonify({"error": "No id"}), 400
    try:
        sb.table("jobs").delete().eq("id", job_id).execute()
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/jobs/clear-all", methods=["POST"])
def clear_all_jobs():
    """Delete every job from Supabase — fresh start."""
    sb = get_supabase()
    if not sb:
        return jsonify({"error": "Supabase not configured"}), 200
    try:
        # Delete all rows — Supabase requires a filter, use neq on a always-true condition
        sb.table("jobs").delete().neq("id", "___never___").execute()
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/generate-docs", methods=["POST"])
def generate_docs():
    """Generate tailored resume + cover letter as .docx files using Node.js script."""
    import subprocess, json as json_lib, tempfile, base64, os

    data = request.json
    role = data.get("role", "").strip()
    company = data.get("company", "").strip()
    jd = data.get("jd", "").strip()
    role_type = data.get("roleType", "").strip()
    is_ai = bool(data.get("isAI", False))

    if not role or not company:
        return jsonify({"error": "role and company are required"}), 400

    with tempfile.TemporaryDirectory() as tmpdir:
        script_path = os.path.join(BASE_DIR, "gen_docs.js")
        payload = json_lib.dumps({
            "role": role,
            "company": company,
            "jd": jd[:3000] if jd else "",
            "roleType": role_type,
            "outputDir": tmpdir,
            "isAI": is_ai
        })

        try:
            result = subprocess.run(
                ["node", script_path, payload],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode != 0:
                return jsonify({"error": result.stderr or "Node script failed"}), 500

            output = json_lib.loads(result.stdout.strip())
            resume_path = output["resume"]
            cover_path = output["cover"]

            with open(resume_path, "rb") as f:
                resume_b64 = base64.b64encode(f.read()).decode()
            with open(cover_path, "rb") as f:
                cover_b64 = base64.b64encode(f.read()).decode()

            return jsonify({
                "resume_b64": resume_b64,
                "cover_b64": cover_b64,
                "variant": output.get("variant", "BA"),
                "resume_filename": f"Resume_{company.replace(' ','_')}.docx",
                "cover_filename": f"CoverLetter_{company.replace(' ','_')}.docx"
            })
        except subprocess.TimeoutExpired:
            return jsonify({"error": "Document generation timed out"}), 500
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@app.route("/api/import-job", methods=["POST"])
def import_job():
    data = request.json
    url = data.get("url", "").strip()
    
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    # Detect platform
    is_linkedin = "linkedin.com" in url
    is_indeed = "indeed.com" in url or "sg.indeed.com" in url

    # Headers that mimic a real browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
    }

    result = {
        "platform": "linkedin" if is_linkedin else "indeed" if is_indeed else "other",
        "url": url,
        "title": "",
        "company": "",
        "location": "Singapore",
        "description": "",
        "partial": False,
        "message": ""
    }

    try:
        from bs4 import BeautifulSoup

        if is_linkedin:
            # LinkedIn blocks login-walled pages but public job URLs sometimes work
            # Extract job ID from URL for reference
            import re
            job_id_match = re.search(r'/jobs/view/(\d+)', url)
            job_id = job_id_match.group(1) if job_id_match else ""
            
            # Try to extract company from URL slug
            company_match = re.search(r'linkedin\.com/jobs/view/[^/]+-at-([a-z0-9-]+)-\d+', url)
            if company_match:
                result["company"] = company_match.group(1).replace("-", " ").title()

            try:
                resp = http_requests.get(url, headers=headers, timeout=10)
                soup = BeautifulSoup(resp.text, "lxml")

                # Try various LinkedIn selectors
                title_el = (soup.find("h1", {"class": lambda c: c and "job-title" in c}) or
                           soup.find("h1", {"class": lambda c: c and "topcard__title" in c}) or
                           soup.find("h1"))
                if title_el:
                    result["title"] = title_el.get_text(strip=True)

                company_el = (soup.find("a", {"class": lambda c: c and "topcard__org-name" in c}) or
                             soup.find("span", {"class": lambda c: c and "company-name" in c}))
                if company_el:
                    result["company"] = company_el.get_text(strip=True)

                desc_el = (soup.find("div", {"class": lambda c: c and "description__text" in c}) or
                          soup.find("div", {"class": lambda c: c and "job-description" in c}))
                if desc_el:
                    result["description"] = desc_el.get_text(separator="\n", strip=True)[:3000]

                if not result["title"] and not result["description"]:
                    # LinkedIn returned a login wall
                    result["partial"] = True
                    result["message"] = "LinkedIn requires login to view full details. Company name extracted from URL — please paste the job description manually."
                else:
                    result["message"] = "Job details imported from LinkedIn!"

            except Exception:
                result["partial"] = True
                result["message"] = "LinkedIn blocked the request. Company extracted from URL — please paste the job description manually."

        elif is_indeed:
            resp = http_requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(resp.text, "lxml")

            # Indeed selectors
            title_el = (soup.find("h1", {"class": lambda c: c and "jobTitle" in str(c)}) or
                       soup.find("h1", {"data-testid": "jobsearch-JobInfoHeader-title"}) or
                       soup.find("h1"))
            if title_el:
                result["title"] = title_el.get_text(strip=True).replace("- job post", "").strip()

            company_el = (soup.find("div", {"data-testid": "inlineHeader-companyName"}) or
                         soup.find("span", {"class": lambda c: c and "companyName" in str(c)}) or
                         soup.find("a", {"data-tn-element": "companyName"}))
            if company_el:
                result["company"] = company_el.get_text(strip=True)

            location_el = (soup.find("div", {"data-testid": "job-location"}) or
                          soup.find("div", {"class": lambda c: c and "companyLocation" in str(c)}))
            if location_el:
                result["location"] = location_el.get_text(strip=True)

            desc_el = (soup.find("div", {"id": "jobDescriptionText"}) or
                      soup.find("div", {"class": lambda c: c and "jobsearch-jobDescriptionText" in str(c)}))
            if desc_el:
                result["description"] = desc_el.get_text(separator="\n", strip=True)[:3000]

            if result["title"] or result["company"]:
                result["message"] = "Job details imported from Indeed! ✅"
            else:
                result["partial"] = True
                result["message"] = "Could not extract details automatically. Please fill in manually."

        else:
            # Generic scrape attempt
            resp = http_requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(resp.text, "lxml")
            title_el = soup.find("h1")
            if title_el:
                result["title"] = title_el.get_text(strip=True)
            result["partial"] = True
            result["message"] = "Basic details extracted — please verify and fill in any missing fields."

    except Exception as e:
        result["partial"] = True
        result["message"] = f"Could not fetch URL automatically. Please fill in details manually. ({str(e)[:80]})"

    return jsonify(result)


@app.route("/api/rank-jobs", methods=["POST"])
def rank_jobs():
    data = request.json
    jobs = data.get("jobs", [])
    
    if not jobs:
        return jsonify({"error": "No jobs provided"}), 400

    # Build a compact job list for the prompt
    job_list = ""
    for i, j in enumerate(jobs):
        jd_snippet = (j.get("jd", "") or "")[:400]
        job_list += f"""
JOB {i+1}:
  ID: {j.get("id")}
  Title: {j.get("role", "Unknown")}
  Company: {j.get("company", "Unknown")}
  Type: {j.get("roleType", "")}
  JD: {jd_snippet if jd_snippet else "No JD provided"}
---"""

    prompt = f"""You are a career coach expert in Singapore's tech and fintech product job market.

CANDIDATE PROFILE:
Name: Amretha Karthikeyan
Current: Lead BA / de-facto Product Owner at KPMG Singapore (Feb 2021–Present)
- Owned Loan IQ core banking product backlog, led cross-functional squads (eng, UX, QA)
- Drove ~5% business value through product scope decisions
- Eliminated 30 man-days via automation feature
- Led sprint ceremonies, PI Planning, go-live planning, data migrations
Certification: SAFe 6.0 Product Owner / Product Manager
Skills: Agile, JIRA, SQL, Tableau, Power BI, Loan IQ, Stakeholder Management, Generative AI, Claude API
Previous: Amazon India (BA, dashboards), J.P. Morgan virtual internship
Personal project: Live AI Trade Analysis platform (Claude Opus 4.6) — proves she ships AI products
Target: In-house product roles in Singapore (NOT consulting) — PM, PO, BA at fintech/tech companies
Experience: 5+ years total
Transition: Consulting → In-house product

JOBS TO EVALUATE:
{job_list}

For each job, return a JSON array with this exact structure:
[
  {{
    "id": <job id number>,
    "score": <integer 1-10>,
    "label": "<one of: 🔥 Strong Match | ✅ Good Fit | 🟡 Possible | ❌ Weak Fit>",
    "reason": "<2 sentences: why she fits + one gap or concern if any>",
    "priority": "<one of: Apply Today | Apply This Week | Lower Priority | Skip>"
  }}
]

Scoring guide:
9-10: Near-perfect fit — in-house product role, fintech/tech domain, Singapore, matches PO/BA background
7-8: Good fit — most criteria match, minor gaps
5-6: Possible — transferable skills apply but some gaps
1-4: Weak fit — significant mismatch in role type, seniority, or domain

COMPANY TYPE WEIGHTING — apply these modifiers BEFORE finalising the score:
+2 points: In-house product companies (Grab, Sea/Shopee, Gojek, Airwallex, Stripe, Revolut, Wise, PropertyGuru, Carousell, Lazada, ByteDance, Razer, DBS Tech, OCBC digital, GovTech, tech startups)
+1 point: Companies with strong internal product teams (large banks with digital arms, insurance tech)
 0 points: Neutral / unclear
-2 points: Consulting or professional services firms (Big 4: KPMG, Deloitte, PwC, EY, Accenture, McKinsey, BCG, Bain, IBM GBS, Wipro, Infosys, TCS, CGI, Cognizant)

Amretha is ACTIVELY LEAVING consulting — a consulting role should score maximum 4/10 regardless of title.
Flag consulting roles clearly in the reason field so she can deprioritise them immediately.

VISA RULE — HARD OVERRIDE:
If the job description contains any of these phrases: "no visa sponsorship", "no sponsorship", "candidates must have right to work", "must be a Singapore citizen or PR", "singaporeans and PRs only", "no work pass sponsorship" — score it 0/10 (zero score), label it ❌ Weak Fit, priority Skip, and reason must say "This role explicitly states no visa sponsorship — not worth applying." regardless of any other fit factors.

Return ONLY the JSON array, no other text."""

    result = call_claude(prompt)
    
    # Parse the JSON response
    import json, re
    try:
        # Clean up response - remove markdown code blocks if present
        clean = re.sub(r'```json|```', '', result).strip()
        rankings = json.loads(clean)
        return jsonify({"rankings": rankings, "raw": result})
    except Exception as e:
        return jsonify({"error": f"Could not parse AI response: {str(e)}", "raw": result}), 500


@app.route("/api/fetch-jd", methods=["POST"])
def fetch_jd():
    """Fetch job description from a LinkedIn or Indeed URL via HTTP scraping."""
    import requests as req
    from bs4 import BeautifulSoup

    data = request.json
    url = (data.get("url") or "").strip()
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "en-US,en;q=0.9",
        }
        resp = req.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(resp.text, "html.parser")

        jd = ""
        title = ""
        company = ""

        if "linkedin.com" in url:
            # LinkedIn job description selectors
            for sel in [
                ".description__text",
                ".show-more-less-html__markup",
                "[class*='description']",
                "section.description",
            ]:
                el = soup.select_one(sel)
                if el and len(el.get_text(strip=True)) > 100:
                    jd = el.get_text(separator="\n", strip=True)[:5000]
                    break

            title_el = soup.select_one("h1.top-card-layout__title, h1[class*='title']")
            if title_el:
                title = title_el.get_text(strip=True)

            company_el = soup.select_one("a.topcard__org-name-link, [class*='company-name']")
            if company_el:
                company = company_el.get_text(strip=True)

        elif "indeed.com" in url:
            for sel in ["#jobDescriptionText", ".jobsearch-jobDescriptionText", "[class*='description']"]:
                el = soup.select_one(sel)
                if el and len(el.get_text(strip=True)) > 100:
                    jd = el.get_text(separator="\n", strip=True)[:5000]
                    break

        elif "mycareersfuture.gov.sg" in url:
            for sel in ["[class*='job-description']", "[class*='description']", "article"]:
                el = soup.select_one(sel)
                if el and len(el.get_text(strip=True)) > 100:
                    jd = el.get_text(separator="\n", strip=True)[:5000]
                    break
        else:
            # Generic fallback
            for tag in soup.find_all(["article", "section", "div"], limit=20):
                text = tag.get_text(strip=True)
                if len(text) > 500 and any(kw in text.lower() for kw in ["responsibilities", "requirements", "qualifications", "experience"]):
                    jd = text[:5000]
                    break

        if not jd:
            return jsonify({"jd": "", "error": "Could not extract JD — LinkedIn may require login"}), 200

        return jsonify({"jd": jd, "title": title, "company": company})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/bookmarklet-add", methods=["POST", "OPTIONS"])
def bookmarklet_add():
    # Handle CORS preflight - bookmarklet calls come from linkedin.com/indeed.com
    if request.method == "OPTIONS":
        response = app.make_default_options_response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        return response

    data = request.json
    role = data.get("role", "").strip()
    company = data.get("company", "").strip()

    if not role or not company:
        resp = jsonify({"success": False, "error": "Missing job title or company"})
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, 400

    # Store in a simple JSON file on the server
    import json, os
    jobs_file = os.path.join(BASE_DIR, "bookmarked_jobs.json")
    
    try:
        if os.path.exists(jobs_file):
            with open(jobs_file, "r") as f:
                saved = json.load(f)
        else:
            saved = []

        new_job = {
            "id": int(__import__("time").time() * 1000),
            "role": role,
            "company": company,
            "jd": data.get("jd", ""),
            "location": data.get("location", "Singapore"),
            "url": data.get("url", ""),
            "status": "wishlist",
            "date": __import__("datetime").date.today().strftime("%d/%m/%Y"),
            "notes": "",
            "salary": "",
            "isDemo": False,
            "fromBookmarklet": True
        }

        saved.append(new_job)
        with open(jobs_file, "w") as f:
            json.dump(saved, f)

        resp = jsonify({"success": True, "job": new_job})
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp

    except Exception as e:
        resp = jsonify({"success": False, "error": str(e)})
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, 500


@app.route("/api/pending-count", methods=["GET"])
def pending_count():
    """Returns how many jobs are queued — does NOT clear the file"""
    import json, os
    jobs_file = os.path.join(BASE_DIR, "bookmarked_jobs.json")
    if not os.path.exists(jobs_file):
        return jsonify({"count": 0})
    try:
        saved = json.load(open(jobs_file))
        return jsonify({"count": len(saved)})
    except:
        return jsonify({"count": 0})


@app.route("/api/bookmarklet-jobs", methods=["GET"])
def bookmarklet_jobs():
    """Frontend calls this to pull queued jobs — clears file after sending"""
    import json, os
    jobs_file = os.path.join(BASE_DIR, "bookmarked_jobs.json")
    if not os.path.exists(jobs_file):
        return jsonify({"jobs": []})
    try:
        with open(jobs_file, "r") as f:
            saved = json.load(f)
        with open(jobs_file, "w") as f:
            json.dump([], f)
        return jsonify({"jobs": saved})
    except Exception as e:
        return jsonify({"jobs": [], "error": str(e)})


@app.route("/api/bookmarklet-bulk", methods=["POST", "OPTIONS"])
def bookmarklet_bulk():
    if request.method == "OPTIONS":
        response = app.make_default_options_response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        return response

    data = request.json
    incoming_jobs = data.get("jobs", [])

    if not incoming_jobs:
        resp = jsonify({"success": False, "error": "No jobs provided"})
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, 400

    import json, os, time
    from datetime import date

    jobs_file = os.path.join(BASE_DIR, "bookmarked_jobs.json")

    try:
        if os.path.exists(jobs_file):
            with open(jobs_file, "r") as f:
                saved = json.load(f)
        else:
            saved = []

        # Avoid duplicates by URL or title+company combo
        seen_urls = set()
        seen_tc   = set()
        for j in saved:
            u = j.get("url","").split("?")[0]
            tc = (j.get("role","").strip().lower() + "|" + j.get("company","").strip().lower())
            if u: seen_urls.add(u)
            seen_tc.add(tc)

        added = 0
        for job in incoming_jobs:
            u  = job.get("url","").split("?")[0]
            tc = (job.get("role","").strip().lower() + "|" + job.get("company","").strip().lower())
            if (u and u in seen_urls) or tc in seen_tc:
                continue
            new_job = {
                "id": int(time.time() * 1000) + added,
                "role": job.get("role", "").strip(),
                "company": job.get("company", "").strip(),
                "jd": job.get("jd", ""),
                "location": job.get("location", "Singapore"),
                "url": job.get("url", ""),
                "status": "wishlist",
                "date": date.today().strftime("%d/%m/%Y"),
                "notes": "",
                "salary": "",
                "isDemo": False,
                "fromBookmarklet": True
            }
            saved.append(new_job)
            if u: seen_urls.add(u)
            seen_tc.add(tc)
            added += 1

        with open(jobs_file, "w") as f:
            json.dump(saved, f)

        resp = jsonify({"success": True, "count": added, "total": len(incoming_jobs)})
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp

    except Exception as e:
        resp = jsonify({"success": False, "error": str(e)})
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, 500


@app.route("/ping")
def ping():
    return "ok", 200


@app.route("/capture")
def capture():
    """Bookmarklet redirects here with job details as URL params"""
    title = request.args.get("title", "").strip()
    company = request.args.get("company", "").strip()
    location = request.args.get("location", "Singapore").strip()
    url = request.args.get("url", "").strip()
    jd = request.args.get("jd", "").strip()

    if not title:
        title = "Unknown Role"
    if not company:
        company = "Unknown Company"

    import json, os, time
    from datetime import date

    jobs_file = os.path.join(BASE_DIR, "bookmarked_jobs.json")
    try:
        existing = json.load(open(jobs_file)) if os.path.exists(jobs_file) else []
    except:
        existing = []

    # Dedup check
    clean_url = url.split("?")[0]
    already = any(j.get("url","").split("?")[0] == clean_url or
                  (j.get("role","") == title and j.get("company","") == company)
                  for j in existing)

    if not already:
        existing.append({
            "id": int(time.time() * 1000),
            "role": title,
            "company": company,
            "location": location,
            "url": url,
            "jd": jd,
            "status": "wishlist",
            "date": date.today().strftime("%d/%m/%Y"),
            "notes": "",
            "salary": "",
            "isDemo": False,
            "fromBookmarklet": True
        })
        with open(jobs_file, "w") as f:
            json.dump(existing, f)
        msg = f"✅ <strong>{title}</strong> at <strong>{company}</strong> added to your Job Tracker!"
        color = "#15803d"
    else:
        msg = f"⚠️ <strong>{title}</strong> at <strong>{company}</strong> is already in your tracker."
        color = "#c2410c"

    app_url = request.host_url.rstrip('/')
    return f"""<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Job Saved!</title>
<style>
  body {{ font-family: -apple-system, sans-serif; background: #f8fafc; display: flex; align-items: center; justify-content: center; min-height: 100vh; margin: 0; }}
  .card {{ background: white; border-radius: 16px; padding: 40px; max-width: 420px; width: 90%; box-shadow: 0 4px 24px rgba(0,0,0,0.1); text-align: center; }}
  h2 {{ color: {color}; margin-bottom: 8px; font-size: 22px; }}
  p {{ color: #64748b; margin-bottom: 24px; font-size: 15px; line-height: 1.5; }}
  .btn {{ display: inline-block; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 15px; cursor: pointer; border: none; margin: 6px; }}
  .btn-primary {{ background: #6366f1; color: white; }}
  .btn-ghost {{ background: #f1f5f9; color: #475569; }}
</style>
</head><body>
<div class="card">
  <div style="font-size:48px;margin-bottom:16px;">{'🎯' if not already else '📌'}</div>
  <h2>{'Job Saved!' if not already else 'Already Saved'}</h2>
  <p>{msg}</p>
  <a href="{app_url}" class="btn btn-primary">Open Job Tracker</a>
  <button onclick="history.back()" class="btn btn-ghost">← Back to LinkedIn</button>
</div>
<script>
  // Auto-close and go back to LinkedIn after 3 seconds if opened in same tab
  setTimeout(function() {{ history.back(); }}, 3000);
</script>
</body></html>"""


@app.route("/capture-bulk", methods=["POST"])
def capture_bulk():
    import json, os, time
    from datetime import date

    raw = request.form.get("jobs", "[]")
    try:
        incoming = json.loads(raw)
    except:
        return "Invalid data", 400

    jobs_file = os.path.join(BASE_DIR, "bookmarked_jobs.json")
    try:
        existing = json.load(open(jobs_file)) if os.path.exists(jobs_file) else []
    except:
        existing = []

    # Build lookup sets for both URL and title+company
    seen_urls = set()
    seen_tc   = set()
    for j in existing:
        u = j.get("url","").split("?")[0]
        tc = (j.get("role","").strip().lower() + "|" + j.get("company","").strip().lower())
        if u: seen_urls.add(u)
        seen_tc.add(tc)

    added = 0
    for job in incoming:
        u  = job.get("url","").split("?")[0]
        tc = (job.get("role","").strip().lower() + "|" + job.get("company","").strip().lower())
        if (u and u in seen_urls) or tc in seen_tc:
            continue
        existing.append({
            "id": int(time.time() * 1000) + added,
            "role": job.get("role","").strip(),
            "company": job.get("company","").strip(),
            "location": job.get("location","Singapore"),
            "url": job.get("url",""),
            "jd": "",
            "status": "wishlist",
            "roleType": job.get("roleType","Business Analyst"),
            "priority": job.get("priority","Medium"),
            "source": "LinkedIn",
            "dateApplied": date.today().isoformat(),
            "notes": "", "salary": "", "isDemo": False,
            "fromBookmarklet": True, "checklist": {}
        })
        if u: seen_urls.add(u)
        seen_tc.add(tc)
        added += 1

    with open(jobs_file, "w") as f:
        json.dump(existing, f)

    # Redirect back to the tracker — user lands there and clicks "Import Pending Jobs"
    return redirect(f"/?imported={added}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
