-- ============================================================
-- Job Hunt App — Supabase Table Setup v2
-- Run in: Supabase Dashboard → SQL Editor → New Query
-- ============================================================

DROP TABLE IF EXISTS jobs;

CREATE TABLE jobs (
  id                   TEXT PRIMARY KEY,
  "linkedInId"         TEXT UNIQUE,
  role                 TEXT,
  company              TEXT,
  url                  TEXT,
  source               TEXT,
  "roleType"           TEXT,
  salary               TEXT,
  notes                TEXT,
  status               TEXT DEFAULT 'saved',
  "dateApplied"        TEXT,
  jd                   TEXT,
  "aiScore"            INTEGER,
  "aiLabel"            TEXT,
  "aiReason"           TEXT,
  "aiPriority"         TEXT,
  resume_docx_b64      TEXT,
  cover_docx_b64       TEXT,
  resume_variant       TEXT,
  resume_filename      TEXT,
  cover_filename       TEXT,
  resume_generated_at  TEXT,
  created_at           TIMESTAMPTZ DEFAULT NOW(),
  updated_at           TIMESTAMPTZ DEFAULT NOW()
);

CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN NEW.updated_at = NOW(); RETURN NEW; END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS set_updated_at ON jobs;
CREATE TRIGGER set_updated_at BEFORE UPDATE ON jobs
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

ALTER TABLE jobs ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all" ON jobs FOR ALL USING (true) WITH CHECK (true);

CREATE UNIQUE INDEX IF NOT EXISTS jobs_linkedin_id_idx ON jobs("linkedInId") WHERE "linkedInId" IS NOT NULL AND "linkedInId" != '';
CREATE INDEX IF NOT EXISTS jobs_created_at_idx ON jobs(created_at DESC);
CREATE INDEX IF NOT EXISTS jobs_status_idx ON jobs(status);
