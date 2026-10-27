// Vercel serverless function: receives website leads and emails them to the SopnoTec inbox
// via Hostinger SMTP. Configure these Environment Variables in Vercel (Project → Settings):
//   SMTP_USER   ab@sopnotec.com                (mailbox that sends the notification)
//   SMTP_PASS   <that mailbox's password>      (never commit this)
//   LEAD_TO     inboxes that receive leads     (optional; comma-separated; defaults below)
//   SMTP_HOST   smtp.hostinger.com             (optional, default shown)
//   SMTP_PORT   465                            (optional, default shown; SSL)
const nodemailer = require('nodemailer');

const DEFAULT_LEAD_TO = 'abubakar@sopnotec.com, ab@sopnotec.com, support@sopnotec.com';

const LIMITS = { name: 120, email: 200, phone: 40, service: 100, subject: 200, message: 5000, page: 300 };
const EMAIL_RE = /^[^\s@<>()[\]\\,;:"]+@[^\s@<>()[\]\\,;:"]+\.[^\s@<>()[\]\\,;:"]{2,}$/;
const SERVICE_NAMES = {
  'customer-service-representative': 'Customer Service Representative',
  'digital-marketing': 'Digital Marketing',
  'live-chat-support-specialist': 'Live Chat Support Specialist',
  'accountant-for-bookkeeping-quickbooks': 'Accountant for Bookkeeping QuickBooks',
  'crm-setup-and-customization': 'CRM Setup and Customization',
  'ticketing-desk-creation': 'Ticketing Desk Creation',
  'campaign-management': 'Campaign Management',
  'cold-caller-call-support': 'Cold Caller / Call Support',
  'social-media-and-linkedin-engagement': 'Social Media and LinkedIn Engagement',
  'wordpress-development': 'WordPress Development',
};

const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const oneLine = (s) => String(s).replace(/[\r\n]+/g, ' ').trim();
const clean = (v, max) => (typeof v === 'string' ? v : v == null ? '' : String(v)).trim().slice(0, max);

let transporter;
function getTransport() {
  if (!transporter) {
    const port = Number(process.env.SMTP_PORT || 465);
    transporter = nodemailer.createTransport({
      host: process.env.SMTP_HOST || 'smtp.hostinger.com',
      port,
      secure: port === 465,
      auth: { user: process.env.SMTP_USER, pass: process.env.SMTP_PASS },
    });
  }
  return transporter;
}

async function readBody(req) {
  if (req.body && typeof req.body === 'object') return req.body;
  let raw = typeof req.body === 'string' ? req.body : '';
  if (!raw) {
    for await (const chunk of req) { raw += chunk; if (raw.length > 50000) break; }
  }
  const type = String(req.headers['content-type'] || '');
  if (type.includes('application/json')) { try { return JSON.parse(raw || '{}'); } catch { return {}; } }
  return Object.fromEntries(new URLSearchParams(raw));
}

function buildEmail(lead, meta) {
  const isNews = lead.form === 'newsletter';
  const svc = SERVICE_NAMES[lead.service] || lead.service;
  const rows = isNews
    ? [['Email', lead.email]]
    : [['Name', lead.name], ['Email', lead.email], ['Phone', lead.phone], ['Service', svc], ['Subject', lead.subject]];
  const extra = [['Page', lead.page], ['Submitted', meta.when], ['IP', meta.ip], ['Browser', meta.ua]];

  const subject = isNews
    ? `New newsletter signup: ${oneLine(lead.email)}`
    : `New lead: ${oneLine(lead.name)}${svc ? ' — ' + oneLine(svc) : ''}${lead.subject ? ' — ' + oneLine(lead.subject) : ''}`.slice(0, 200);

  const tr = (k, v) => `<tr><td style="padding:8px 12px;color:#6b7280;white-space:nowrap;vertical-align:top">${esc(k)}</td><td style="padding:8px 12px;color:#111827">${esc(v || '—')}</td></tr>`;
  const html = `<div style="font-family:Arial,Helvetica,sans-serif;max-width:640px;margin:auto;border:1px solid #e5e7eb;border-radius:10px;overflow:hidden">
<div style="background:#5b6ee1;color:#fff;padding:16px 20px;font-size:18px;font-weight:bold">${isNews ? 'New newsletter signup' : 'New website lead'} · SopnoTec</div>
<table style="width:100%;border-collapse:collapse;font-size:14px">${rows.map(([k, v]) => tr(k, v)).join('')}</table>
${!isNews ? `<div style="padding:12px 20px"><div style="color:#6b7280;font-size:13px;margin-bottom:6px">Message</div><div style="white-space:pre-wrap;font-size:14px;color:#111827;background:#f9fafb;border-radius:8px;padding:12px">${esc(lead.message || '—')}</div></div>` : ''}
<table style="width:100%;border-collapse:collapse;font-size:12px;border-top:1px solid #e5e7eb">${extra.map(([k, v]) => tr(k, v)).join('')}</table>
<div style="padding:12px 20px;font-size:12px;color:#6b7280">Hit <b>Reply</b> to answer ${esc(lead.name || lead.email)} directly.</div></div>`;

  const text = [isNews ? 'New newsletter signup' : 'New website lead', '',
    ...rows.map(([k, v]) => `${k}: ${v || '-'}`),
    ...(isNews ? [] : ['', 'Message:', lead.message || '-']),
    '', ...extra.map(([k, v]) => `${k}: ${v || '-'}`)].join('\n');

  return { subject, html, text };
}

module.exports = async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method !== 'POST') { res.setHeader('Allow', 'POST'); return res.status(405).json({ ok: false, error: 'Method not allowed' }); }

  const b = await readBody(req);
  // Spam traps: hidden "website" field must be empty; real people take more than ~2s to fill the form.
  if (clean(b.website, 200) || (b.elapsed !== undefined && Number(b.elapsed) < 2000)) {
    return res.status(200).json({ ok: true });
  }

  const lead = { form: b.form === 'newsletter' ? 'newsletter' : 'contact' };
  for (const k of Object.keys(LIMITS)) lead[k] = clean(b[k], LIMITS[k]);

  if (!EMAIL_RE.test(lead.email)) return res.status(400).json({ ok: false, error: 'Please enter a valid email address.' });
  if (lead.form === 'contact' && !lead.name) return res.status(400).json({ ok: false, error: 'Please enter your name.' });

  if (!process.env.SMTP_USER || !process.env.SMTP_PASS) {
    console.error('lead: SMTP_USER / SMTP_PASS not configured');
    return res.status(500).json({ ok: false, error: 'Our form is temporarily unavailable.' });
  }

  const meta = {
    when: new Date().toLocaleString('en-US', { timeZone: 'Asia/Karachi', dateStyle: 'medium', timeStyle: 'short' }) + ' (PKT)',
    ip: oneLine(String(req.headers['x-forwarded-for'] || '').split(',')[0]),
    ua: oneLine(String(req.headers['user-agent'] || '')).slice(0, 200),
  };
  const { subject, html, text } = buildEmail(lead, meta);

  try {
    await getTransport().sendMail({
      from: { name: 'SopnoTec Website', address: process.env.SMTP_USER },
      to: process.env.LEAD_TO || DEFAULT_LEAD_TO,
      replyTo: lead.name ? { name: oneLine(lead.name), address: lead.email } : lead.email,
      subject, text, html,
    });
    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error('lead: send failed', err && err.message);
    return res.status(502).json({ ok: false, error: 'We could not send your message right now.' });
  }
};

module.exports.buildEmail = buildEmail;
