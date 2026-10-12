/* StudySpark client script: small, dependency-free. */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const csrf = $('meta[name="csrf-token"]')?.content || '';
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

  async function api(url, method = 'POST', body) {
    const res = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json', 'X-CSRF-Token': csrf },
      body: body ? JSON.stringify(body) : undefined,
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      if (res.status === 401) location.href = '/login';
      throw new Error(data.error || 'Something went wrong.');
    }
    return data;
  }

  function toast(msg) {
    const el = document.createElement('div');
    el.className = 'toast';
    el.textContent = msg;
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 3000);
  }

  /* Scroll-in animation */
  const reveals = $$('.reveal');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.08 });
    reveals.forEach((el, i) => { el.style.transitionDelay = Math.min(i * 40, 240) + 'ms'; io.observe(el); });
  } else {
    reveals.forEach((el) => el.classList.add('in'));
  }

  /* Progress checkboxes (syllabus + map work) */
  $$('.js-progress').forEach((box) => {
    box.addEventListener('change', async () => {
      const want = box.checked;
      try {
        await api('/api/progress', 'POST', { key: box.dataset.key, done: want });
        box.dispatchEvent(new CustomEvent('saved', { bubbles: true }));
      } catch (err) {
        box.checked = !want;
        toast(err.message);
      }
    });
  });

  /* Syllabus page */
  const tabs = $('#subjectTabs');
  if (tabs) {
    const panels = $$('.panel');
    const search = $('#search');
    const status = $('#status');
    const names = panels.map((p) => p.dataset.panel);
    const fromHash = decodeURIComponent(location.hash.slice(1));
    let active = names.includes(fromHash) ? fromHash : names[0];

    function counts() {
      const boxes = $$('.panel .js-progress');
      const done = boxes.filter((b) => b.checked).length;
      const pct = boxes.length ? Math.round((done / boxes.length) * 100) : 0;
      boxes.forEach((b) => {
        const pill = b.closest('.item').querySelector('.pill');
        pill.textContent = b.checked ? 'Done' : 'To do';
        pill.classList.toggle('ok', b.checked);
      });
      $('#overallBar').style.width = pct + '%';
      $('#overallPill').textContent = pct + '% complete';
      $('#overallText').textContent = `${done} of ${boxes.length} topics done`;
    }

    function filter() {
      const term = search.value.trim().toLowerCase();
      const st = status.value;
      panels.forEach((p) => {
        p.hidden = p.dataset.panel !== active;
        if (p.hidden) return;
        $$('.group', p).forEach((g) => {
          let visible = 0;
          $$('.item', g).forEach((it) => {
            const done = $('input', it).checked;
            const ok = (!term || it.textContent.toLowerCase().includes(term)) &&
                       (st === 'all' || (st === 'done') === done);
            it.hidden = !ok;
            if (ok) visible++;
          });
          g.hidden = !visible;
        });
        $('.none', p).hidden = $$('.item:not([hidden])', p).length > 0;
      });
      $$('.tab', tabs).forEach((t) => t.classList.toggle('active', t.dataset.subject === active));
    }

    tabs.addEventListener('click', (e) => {
      const t = e.target.closest('.tab');
      if (!t) return;
      active = t.dataset.subject;
      filter();
    });
    search.addEventListener('input', filter);
    status.addEventListener('change', filter);
    document.addEventListener('saved', () => { counts(); filter(); });
    counts();
    filter();
  }

  /* Map work counter */
  const mapCount = $('#mapCount');
  if (mapCount) {
    const update = () => {
      mapCount.textContent = $$('#maps .js-progress').filter((b) => b.checked).length + ' completed';
    };
    document.addEventListener('saved', update);
    update();
  }

  /* Dashboard: daily checklist (resets each day, stored on this device) */
  const tasks = $$('[data-task]');
  if (tasks.length) {
    const day = new Date().toISOString().slice(0, 10);
    const k = (n) => `ss-task:${day}:${n}`;
    const read = (key) => { try { return localStorage.getItem(key); } catch { return null; } };
    const write = (key, v) => { try { v ? localStorage.setItem(key, '1') : localStorage.removeItem(key); } catch { /* ignore */ } };
    tasks.forEach((c) => {
      c.checked = read(k(c.dataset.task)) === '1';
      c.addEventListener('change', () => write(k(c.dataset.task), c.checked));
    });
    $('#resetTasks')?.addEventListener('click', () => tasks.forEach((c) => { c.checked = false; write(k(c.dataset.task), false); }));
  }

  /* Dashboard: focus timer */
  const display = $('#timerDisplay');
  if (display) {
    const FULL = 25 * 60;
    let seconds = FULL, timer = null, running = false;
    const msg = $('#timerMessage'), toggle = $('#timerToggle');
    const draw = () => {
      display.textContent = String(Math.floor(seconds / 60)).padStart(2, '0') + ':' + String(seconds % 60).padStart(2, '0');
      document.title = running ? `${display.textContent} · StudySpark` : document.title.replace(/^\d\d:\d\d · /, '');
    };
    const stop = () => { clearInterval(timer); running = false; };
    toggle.addEventListener('click', () => {
      if (running) {
        stop(); toggle.textContent = 'Resume'; msg.textContent = 'Paused. Restart whenever you’re ready.';
      } else {
        running = true; toggle.textContent = 'Pause'; msg.textContent = 'Focus mode on. One thing at a time.';
        timer = setInterval(() => {
          if (seconds > 0) { seconds--; draw(); return; }
          stop(); toggle.textContent = 'Start'; seconds = FULL;
          msg.textContent = 'Nice work! Session complete. Take a short break.';
          if (navigator.vibrate) navigator.vibrate(150);
          draw();
        }, 1000);
      }
      draw();
    });
    $('#timerReset').addEventListener('click', () => {
      stop(); seconds = FULL; toggle.textContent = 'Start'; msg.textContent = 'Timer reset. Ready when you are.'; draw();
    });
    draw();
  }

  /* Practice quiz */
  const quizEl = $('#quiz');
  if (quizEl) {
    const all = JSON.parse($('#quiz-data').textContent);
    const subjectSel = $('#quizSubject');
    let set = [], i = 0, score = 0, answered = false;

    function start() {
      const sub = subjectSel.value;
      set = all.filter((q) => sub === 'all' || q.subject === sub);
      i = 0; score = 0;
      $('#quizScore').textContent = 'Score: 0';
      $('#checkQuiz').hidden = false;
      $('#nextQuiz').textContent = 'Next →';
      draw();
    }

    function draw() {
      const answers = $('#quizAnswers');
      $('#quizFeedback').textContent = '';
      if (!set.length) {
        $('#quizQuestion').textContent = 'No questions for this subject yet.';
        answers.innerHTML = '';
        return;
      }
      const q = set[i];
      answered = false;
      $('#checkQuiz').disabled = false;
      $('#quizCounter').textContent = `${q.subject} · Question ${i + 1} of ${set.length}`;
      $('#quizQuestion').textContent = q.q;
      answers.innerHTML = q.a.map((a, n) =>
        `<label class="answer"><input type="radio" name="ans" value="${n}"> ${String.fromCharCode(65 + n)}. ${esc(a)}</label>`).join('');
    }

    async function finish() {
      $('#quizCounter').textContent = 'All done';
      $('#quizQuestion').textContent = `You scored ${score} out of ${set.length}.`;
      $('#quizAnswers').innerHTML = '';
      $('#quizFeedback').textContent = score === set.length ? 'Perfect round!' : 'Nice effort. Try again to beat your score.';
      $('#checkQuiz').hidden = true;
      $('#nextQuiz').textContent = 'Restart';
      try { await api('/api/quiz', 'POST', { subject: subjectSel.value, score, total: set.length }); }
      catch (err) { toast(err.message); }
    }

    $('#checkQuiz').addEventListener('click', () => {
      if (answered || !set.length) return;
      const picked = $('input[name="ans"]:checked');
      if (!picked) { $('#quizFeedback').textContent = 'Choose an answer first 🙂'; return; }
      answered = true;
      const q = set[i];
      const ok = Number(picked.value) === q.correct;
      if (ok) score++;
      $$('.answer').forEach((el, n) => {
        if (n === q.correct) el.classList.add('right');
        else if (el.contains(picked)) el.classList.add('wrong');
      });
      $('#quizScore').textContent = 'Score: ' + score;
      $('#quizFeedback').textContent = (ok ? 'Correct! ' : 'Not quite. ') + q.why;
      $('#checkQuiz').disabled = true;
    });

    $('#nextQuiz').addEventListener('click', () => {
      if (!set.length) return;
      if (i >= set.length - 1 && answered) { i++; return finish(); }
      if ($('#checkQuiz').hidden) return start();
      if (i < set.length - 1) { i++; draw(); }
      else if (answered) finish();
      else $('#quizFeedback').textContent = 'Check your answer first, then finish.';
    });
    subjectSel.addEventListener('change', start);
    start();
  }

  /* Planner */
  const list = $('#planList');
  if (list) {
    let plans = JSON.parse($('#plans-data').textContent);
    const msg = $('#planMessage');

    function render() {
      if (!plans.length) { list.innerHTML = '<p class="tiny">No tasks yet. Add your first study task.</p>'; return; }
      list.innerHTML = plans.map((p) => `
        <div class="planitem" data-id="${esc(p.id)}">
          <label class="task"><input type="checkbox" ${p.done ? 'checked' : ''}>
            <span><b>${esc(p.task)}</b><br><span class="tiny">${esc(p.subject)}${p.due_date ? ' · ' + esc(p.due_date) : ''}</span></span>
          </label>
          <button class="btn small" type="button" data-del aria-label="Delete task">✕</button>
        </div>`).join('');
    }

    list.addEventListener('change', async (e) => {
      const row = e.target.closest('.planitem');
      if (!row) return;
      const plan = plans.find((p) => p.id === row.dataset.id);
      const want = e.target.checked;
      try { await api('/api/plans/' + plan.id, 'PATCH', { done: want }); plan.done = want; }
      catch (err) { e.target.checked = !want; toast(err.message); }
    });

    list.addEventListener('click', async (e) => {
      if (!e.target.closest('[data-del]')) return;
      const row = e.target.closest('.planitem');
      try {
        await api('/api/plans/' + row.dataset.id, 'DELETE');
        plans = plans.filter((p) => p.id !== row.dataset.id);
        render();
      } catch (err) { toast(err.message); }
    });

    $('#planForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      const task = $('#planTask').value.trim();
      if (!task) { msg.textContent = 'Enter a task first.'; return; }
      try {
        const row = await api('/api/plans', 'POST', {
          task, subject: $('#planSubject').value, due_date: $('#planDate').value || null,
        });
        plans.push(row);
        $('#planTask').value = '';
        msg.textContent = 'Task added!';
        render();
      } catch (err) { msg.textContent = err.message; }
    });

    render();
  }
})();
