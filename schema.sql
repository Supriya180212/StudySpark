-- StudySpark schema for Supabase. Paste into: Supabase dashboard -> SQL Editor -> Run.
-- Users live in Supabase Auth (auth.users); these tables hang off them.

create extension if not exists "pgcrypto";

-- Which syllabus topics / map items each student has ticked off
create table if not exists public.progress (
  user_id    uuid    not null references auth.users(id) on delete cascade,
  item_key   text    not null,
  done       boolean not null default false,
  updated_at timestamptz not null default now(),
  primary key (user_id, item_key)
);

-- Study planner tasks
create table if not exists public.plans (
  id         uuid primary key default gen_random_uuid(),
  user_id    uuid not null references auth.users(id) on delete cascade,
  task       text not null check (char_length(task) between 1 and 200),
  subject    text not null,
  due_date   date,
  done       boolean not null default false,
  created_at timestamptz not null default now()
);
create index if not exists plans_user_idx on public.plans (user_id, created_at);

-- Finished practice quizzes
create table if not exists public.quiz_attempts (
  id         uuid primary key default gen_random_uuid(),
  user_id    uuid not null references auth.users(id) on delete cascade,
  subject    text not null,
  score      int  not null check (score >= 0),
  total      int  not null check (total > 0),
  created_at timestamptz not null default now()
);
create index if not exists quiz_user_idx on public.quiz_attempts (user_id, created_at desc);

-- Row Level Security: a signed-in user can only ever touch their own rows.
-- (The Flask server uses the service-role key, which bypasses RLS, and also
-- filters every query by user_id. RLS is the safety net for any direct access.)
alter table public.progress      enable row level security;
alter table public.plans         enable row level security;
alter table public.quiz_attempts enable row level security;

drop policy if exists "own progress" on public.progress;
create policy "own progress" on public.progress
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

drop policy if exists "own plans" on public.plans;
create policy "own plans" on public.plans
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

drop policy if exists "own quiz attempts" on public.quiz_attempts;
create policy "own quiz attempts" on public.quiz_attempts
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
