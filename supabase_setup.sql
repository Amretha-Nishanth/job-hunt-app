-- ============================================================
-- Job Hunt App — Supabase Table Setup
-- Run this in: Supabase Dashboard → SQL Editor → New Query
-- ============================================================

-- Drop existing table if you want a completely fresh start
-- (Only uncomment if you want to wipe everything)
-- DROP TABLE IF EXISTS jobs;

-- Create jobs table with ALL fields the app uses
CREATE TABLE IF NOT EXISTS jobs (
  -- Identity
  id                   TEXT PRIMARY KEY,
  role                 TEXT,
  company              TEXT,

  -- Status & tracking
  status               TEXT DEFAULT 'saved',
  dateApplied          TEXT,
  source               TEXT,
  url                  TEXT,
  salary               TEXT,
  roleType             TEXT,
  notes                TEXT,

  -- Job description (up to 8000 chars)
  jd                   TEXT,

  -- AI scoring
  "aiScore"            INTEGER,
  "aiLabel"            TEXT,
  "aiReason"           TEXT,
  "aiPriority"         TEXT,

  -- Generated documents (base64 encoded .docx)
  resume_docx_b64      TEXT,
  cover_docx_b64       TEXT,
  resume_variant       TEXT,
  resume_filename      TEXT,
  cover_filename       TEXT,
  resume_generated_at  TEXT,

  -- Timestamps
  created_at           TIMESTAMPTZ DEFAULT NOW(),
  updated_at           TIMESTAMPTZ DEFAULT NOW()
);

-- Auto-update updated_at on every change
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS set_updated_at ON jobs;
CREATE TRIGGER set_updated_at
  BEFORE UPDATE ON jobs
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- Enable Row Level Security (keeps your data private)
ALTER TABLE jobs ENABLE ROW LEVEL SECURITY;

-- Allow all operations from your backend (using service role / anon key)
CREATE POLICY "Allow all" ON jobs FOR ALL USING (true) WITH CHECK (true);

-- Useful index for sorting by created date
CREATE INDEX IF NOT EXISTS jobs_created_at_idx ON jobs(created_at DESC);

-- ============================================================
-- VERIFY: After running, you should see the jobs table
-- in Database → Tables with all these columns
-- ============================================================
