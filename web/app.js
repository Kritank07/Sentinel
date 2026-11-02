// Sentinel — shared helpers: language, translations, API calls and the verdict sheet.
// The chosen language also decides the language of Sentinel's answers.

const I18N = {
  English: {
    "intro.title": "Check anything that feels like a scam.",
    "intro.body": "Sentinel reads, listens and looks for the tricks scammers use, then tells you exactly what to do.",
    "call.title": "Protect a live call",
    "call.body": "Sentinel listens while you talk and warns you the moment someone asks for money or an OTP.",
    "call.cta": "Start protection",
    "voice.title": "Check a voice note",
    "voice.body": "Find out if a recording is a scam, and whether the voice is real or made by AI.",
    "screenshot.title": "Check a screenshot",
    "screenshot.body": "See exactly where the fraud is in a message, payment proof or video call.",
    "message.title": "Check a message or link",
    "message.body": "Paste an SMS, email or WhatsApp forward. Sentinel checks every link and number in it.",
    "footer.models": "Built on Meta Muse Wonder, Muse Spark, Muse Voice Transcribe and SAM 3.1.",
    "footer.help": "Lost money to a scam in India? Call 1930 or report at cybercrime.gov.in.",
    "footer.tagline": "A second opinion before you pay, click or share.",
    "footer.checks": "Checks",
    "footer.needHelp": "Need help now?",
    "footer.call1930": "Call 1930 (India cyber fraud helpline)",
    "footer.report": "Report at cybercrime.gov.in",
    "footer.built": "Built by Kritank Jain.",
    "footer.source": "Source code",
    "footer.disclaimer": "Sentinel gives safety guidance, not legal or financial advice. If you are in danger, contact your local police.",

    "nav.all": "All checks",
    "message.lead": "Paste the message, or add a screenshot of it. Sentinel reads it for you.",
    "message.attach": "Add screenshot",
    "message.attachHint": "or paste or drop an image here",
    "message.remove": "Remove screenshot",
    "loading.screenshot": "Reading the screenshot…",
    "error.imageType": "Use a PNG or JPG image.",
    "screenshot.lead": "Add a screenshot of a message, payment proof, ID card or video call.",
    "screenshot.drop": "Drop a screenshot here, paste it, or choose a file.",
    "screenshot.choose": "Choose screenshot",
    "screenshot.check": "Check screenshot",
    "loading.look": "Looking at the screenshot…",
    "loading.mark": "Marking the evidence…",
    "label.evidence": "Where the fraud is",
    "source.sam": "Located by SAM 3.1",
    "source.wonder": "Located by Muse Wonder",
    "error.noImage": "Add a screenshot first.",
    "voice.lead": "Upload a voice note or call recording, or record one here.",
    "voice.drop": "Drop an audio file here, or choose one. WhatsApp voice notes work too.",
    "voice.choose": "Choose audio file",
    "voice.or": "or",
    "voice.record": "Record",
    "voice.stop": "Stop recording",
    "voice.remove": "Remove audio",
    "voice.check": "Check voice note",
    "loading.prepare": "Preparing the audio…",
    "loading.listen": "Listening to the recording…",
    "loading.voice": "Checking if the voice is real…",
    "label.voice": "Is the voice real?",
    "voice.REAL": "Sounds like a real person",
    "voice.UNCERTAIN": "Can't tell for sure",
    "voice.AI_GENERATED": "Sounds AI-made or cloned",
    "voice.likelihood": "Chance the voice is AI-made",
    "voice.note": "A voice check is one clue, not proof. New cloning tools can sound very real.",
    "label.transcript": "What was said",
    "speaker": "Speaker",
    "error.noAudio": "Add or record a voice note first.",
    "error.audioType": "This audio file couldn't be read. Try an MP3, WAV, M4A or OGG file.",
    "error.mic": "Microphone access was blocked. Allow it in your browser settings, then try again.",
    "error.tooLong": "Use a recording under 10 minutes.",
    "call.lead": "Put the call on speaker near this device, then start protection. Sentinel listens and warns you if something is wrong.",
    "call.end": "End call",
    "call.start": "Start call",
    "call.connecting": "Connecting…",
    "call.listening": "Listening",
    "call.waiting": "Sentinel is listening. Warnings will appear here.",
    "call.transcript": "Live conversation",
    "call.scammer": "Possible scammer",
    "call.other": "Other speaker",
    "call.stopTitle": "STOP",
    "call.ok": "Okay",
    "call.ended": "Protection ended.",
    "call.again": "Start call again",
    "call.lost": "The connection was lost. Start protection again.",
    "call.tip": "Never share an OTP, PIN or password on a call, even with someone who says they are police or your bank.",
    "message.label": "Message to check",
    "message.placeholder": "Paste the message here…",
    "message.check": "Check message",
    "examples.label": "Try an example:",
    "example.kyc": "Bank KYC alert",
    "example.parcel": "Parcel fee",
    "example.family": "Message from family",

    "loading.read": "Reading the message…",
    "loading.links": "Checking every link…",
    "loading.search": "Looking for scam reports…",
    "loading.write": "Writing your answer…",

    "verdict.SCAM": "This is a scam.",
    "verdict.SUSPICIOUS": "Be careful. This looks suspicious.",
    "verdict.SAFE": "This looks safe.",
    "label.risk": "Risk",
    "label.action": "What to do now",
    "label.why": "Why",
    "label.signs": "Warning signs",
    "label.checked": "What Sentinel checked",
    "tool.link": "Link check",
    "tool.search": "Web search",
    "tool.other": "Check",

    "error.empty": "Paste a message or add a screenshot first.",
    "error.generic": "The check couldn't finish. Try again in a moment.",
  },
  Hindi: {
    "intro.title": "जो भी धोखा लगे, उसे यहाँ जाँचें।",
    "intro.body": "Sentinel ठगों की चालें पढ़कर, सुनकर और देखकर पहचानता है, और बताता है कि अब आपको क्या करना है।",
    "call.title": "चल रही कॉल को सुरक्षित करें",
    "call.body": "बात करते समय Sentinel सुनता रहता है और जैसे ही कोई पैसे या OTP माँगे, आपको तुरंत सावधान करता है।",
    "call.cta": "सुरक्षा शुरू करें",
    "voice.title": "वॉइस नोट जाँचें",
    "voice.body": "पता करें कि रिकॉर्डिंग धोखा है या नहीं, और आवाज़ असली है या AI से बनी है।",
    "screenshot.title": "स्क्रीनशॉट जाँचें",
    "screenshot.body": "मैसेज, पेमेंट प्रूफ़ या वीडियो कॉल में धोखा कहाँ है, सीधे देखें।",
    "message.title": "मैसेज या लिंक जाँचें",
    "message.body": "SMS, ईमेल या WhatsApp फ़ॉरवर्ड पेस्ट करें। Sentinel उसमें हर लिंक और नंबर की जाँच करता है।",
    "footer.models": "Meta Muse Wonder, Muse Spark, Muse Voice Transcribe और SAM 3.1 पर बना।",
    "footer.help": "भारत में ठगी हुई है? 1930 पर कॉल करें या cybercrime.gov.in पर शिकायत करें।",
    "footer.tagline": "पैसे भेजने, क्लिक करने या जानकारी देने से पहले एक दूसरी राय।",
    "footer.checks": "जाँचें",
    "footer.needHelp": "अभी मदद चाहिए?",
    "footer.call1930": "1930 पर कॉल करें (साइबर ठगी हेल्पलाइन)",
    "footer.report": "cybercrime.gov.in पर शिकायत करें",
    "footer.built": "Kritank Jain द्वारा बनाया गया।",
    "footer.source": "सोर्स कोड",
    "footer.disclaimer": "Sentinel सुरक्षा से जुड़ी सलाह देता है, क़ानूनी या वित्तीय सलाह नहीं। अगर आप ख़तरे में हैं, तो स्थानीय पुलिस से संपर्क करें।",

    "nav.all": "सभी जाँचें",
    "message.lead": "मैसेज पेस्ट करें या उसका स्क्रीनशॉट जोड़ें। Sentinel उसे आपके लिए पढ़ लेगा।",
    "message.attach": "स्क्रीनशॉट जोड़ें",
    "message.attachHint": "या इमेज यहाँ पेस्ट या ड्रॉप करें",
    "message.remove": "स्क्रीनशॉट हटाएँ",
    "loading.screenshot": "स्क्रीनशॉट पढ़ा जा रहा है…",
    "error.imageType": "PNG या JPG इमेज इस्तेमाल करें।",
    "screenshot.lead": "मैसेज, पेमेंट प्रूफ़, पहचान पत्र या वीडियो कॉल का स्क्रीनशॉट जोड़ें।",
    "screenshot.drop": "स्क्रीनशॉट यहाँ ड्रॉप करें, पेस्ट करें या फ़ाइल चुनें।",
    "screenshot.choose": "स्क्रीनशॉट चुनें",
    "screenshot.check": "स्क्रीनशॉट जाँचें",
    "loading.look": "स्क्रीनशॉट देखा जा रहा है…",
    "loading.mark": "सबूत चिह्नित किए जा रहे हैं…",
    "label.evidence": "धोखा कहाँ है",
    "source.sam": "SAM 3.1 ने ढूँढा",
    "source.wonder": "Muse Wonder ने ढूँढा",
    "error.noImage": "पहले स्क्रीनशॉट जोड़ें।",
    "voice.lead": "वॉइस नोट या कॉल रिकॉर्डिंग अपलोड करें, या यहीं रिकॉर्ड करें।",
    "voice.drop": "ऑडियो फ़ाइल यहाँ ड्रॉप करें या चुनें। WhatsApp वॉइस नोट भी चलेंगे।",
    "voice.choose": "ऑडियो फ़ाइल चुनें",
    "voice.or": "या",
    "voice.record": "रिकॉर्ड करें",
    "voice.stop": "रिकॉर्डिंग रोकें",
    "voice.remove": "ऑडियो हटाएँ",
    "voice.check": "वॉइस नोट जाँचें",
    "loading.prepare": "ऑडियो तैयार हो रहा है…",
    "loading.listen": "रिकॉर्डिंग सुनी जा रही है…",
    "loading.voice": "आवाज़ असली है या नहीं, जाँचा जा रहा है…",
    "label.voice": "क्या आवाज़ असली है?",
    "voice.REAL": "असली इंसान की आवाज़ लगती है",
    "voice.UNCERTAIN": "पक्का नहीं कहा जा सकता",
    "voice.AI_GENERATED": "AI से बनी या नकली (क्लोन) आवाज़ लगती है",
    "voice.likelihood": "आवाज़ के AI से बने होने की संभावना",
    "voice.note": "आवाज़ की जाँच सिर्फ़ एक संकेत है, पक्का सबूत नहीं। नए क्लोनिंग टूल बहुत असली लग सकते हैं।",
    "label.transcript": "क्या कहा गया",
    "speaker": "वक्ता",
    "error.noAudio": "पहले वॉइस नोट जोड़ें या रिकॉर्ड करें।",
    "error.audioType": "यह ऑडियो फ़ाइल पढ़ी नहीं जा सकी। MP3, WAV, M4A या OGG फ़ाइल आज़माएँ।",
    "error.mic": "माइक्रोफ़ोन की अनुमति नहीं मिली। ब्राउज़र सेटिंग में अनुमति दें और फिर कोशिश करें।",
    "error.tooLong": "10 मिनट से छोटी रिकॉर्डिंग इस्तेमाल करें।",
    "call.lead": "कॉल को स्पीकर पर रखें और इस डिवाइस के पास रखें, फिर सुरक्षा शुरू करें। Sentinel सुनता रहेगा और कुछ गलत होने पर आपको सावधान करेगा।",
    "call.end": "कॉल बंद करें",
    "call.start": "कॉल शुरू करें",
    "call.connecting": "जुड़ रहा है…",
    "call.listening": "सुन रहा है",
    "call.waiting": "Sentinel सुन रहा है। चेतावनियाँ यहाँ दिखेंगी।",
    "call.transcript": "चल रही बातचीत",
    "call.scammer": "संभावित ठग",
    "call.other": "दूसरा वक्ता",
    "call.stopTitle": "रुकिए!",
    "call.ok": "ठीक है",
    "call.ended": "सुरक्षा बंद हो गई।",
    "call.again": "कॉल फिर से शुरू करें",
    "call.lost": "कनेक्शन टूट गया। सुरक्षा फिर से शुरू करें।",
    "call.tip": "कॉल पर कभी भी OTP, PIN या पासवर्ड न बताएँ, चाहे सामने वाला ख़ुद को पुलिस या बैंक का बताए।",
    "message.label": "जाँचने के लिए मैसेज",
    "message.placeholder": "मैसेज यहाँ पेस्ट करें…",
    "message.check": "मैसेज जाँचें",
    "examples.label": "उदाहरण आज़माएँ:",
    "example.kyc": "बैंक KYC अलर्ट",
    "example.parcel": "पार्सल शुल्क",
    "example.family": "परिवार का मैसेज",

    "loading.read": "मैसेज पढ़ा जा रहा है…",
    "loading.links": "हर लिंक की जाँच हो रही है…",
    "loading.search": "ठगी की शिकायतें खोजी जा रही हैं…",
    "loading.write": "आपका जवाब तैयार हो रहा है…",

    "verdict.SCAM": "यह धोखा है।",
    "verdict.SUSPICIOUS": "सावधान रहें। यह संदिग्ध लगता है।",
    "verdict.SAFE": "यह सुरक्षित लगता है।",
    "label.risk": "ख़तरा",
    "label.action": "अब क्या करें",
    "label.why": "क्यों",
    "label.signs": "ख़तरे के संकेत",
    "label.checked": "Sentinel ने क्या जाँचा",
    "tool.link": "लिंक की जाँच",
    "tool.search": "वेब खोज",
    "tool.other": "जाँच",

    "error.empty": "पहले मैसेज पेस्ट करें या स्क्रीनशॉट जोड़ें।",
    "error.generic": "जाँच पूरी नहीं हो सकी। थोड़ी देर बाद फिर कोशिश करें।",
  },
};

/* ---------- Language ---------- */

function getLang() {
  try {
    return localStorage.getItem("sentinel-lang") || "English";
  } catch {
    return "English";
  }
}

function setLang(lang) {
  try {
    localStorage.setItem("sentinel-lang", lang);
  } catch { /* storage unavailable: language resets on reload */ }
  applyI18n();
}

function t(key, fallback) {
  return (I18N[getLang()] || {})[key] ?? I18N.English[key] ?? fallback ?? "";
}

function applyI18n() {
  const lang = getLang();
  document.documentElement.lang = lang === "Hindi" ? "hi" : "en";
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    if (el.dataset.i18nDefault === undefined) el.dataset.i18nDefault = el.textContent.trim();
    el.textContent = t(el.dataset.i18n, el.dataset.i18nDefault);
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach((el) => {
    el.placeholder = t(el.dataset.i18nPlaceholder);
  });
  document.querySelectorAll("[data-lang]").forEach((btn) => {
    btn.setAttribute("aria-pressed", String(btn.dataset.lang === lang));
  });
}

document.addEventListener("DOMContentLoaded", () => {
  renderFooter();
  document.querySelectorAll("[data-lang]").forEach((btn) => {
    btn.addEventListener("click", () => setLang(btn.dataset.lang));
  });
  applyI18n();
});

/* ---------- Shared footer (edit here once, every page updates) ---------- */

const REPO_URL = "";   // add your GitHub repo link here later; the "Source code" link appears only when this is set

function renderFooter() {
  const footer = document.getElementById("site-footer");
  if (!footer) return;
  footer.innerHTML = `
    <div class="footer-inner">
      <div class="footer-brand">
        <a class="brand" href="index.html">
          <svg viewBox="0 0 24 24" width="26" height="26" fill="none" aria-hidden="true">
            <path d="M12 2.5 4 5.5v6.2c0 4.6 3.3 8.6 8 9.8 4.7-1.2 8-5.2 8-9.8V5.5l-8-3Z" fill="#EDE8F0"/>
            <path d="M8.5 12.2 11 14.6l4.6-5" stroke="#2F1F3A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          Sentinel
        </a>
        <p data-i18n="footer.tagline">A second opinion before you pay, click or share.</p>
      </div>
      <nav class="footer-col" aria-labelledby="footer-checks">
        <h2 id="footer-checks" data-i18n="footer.checks">Checks</h2>
        <a href="call.html" data-i18n="call.title">Protect a live call</a>
        <a href="voice.html" data-i18n="voice.title">Check a voice note</a>
        <a href="screenshot.html" data-i18n="screenshot.title">Check a screenshot</a>
        <a href="message.html" data-i18n="message.title">Check a message or link</a>
      </nav>
      <div class="footer-col">
        <h2 data-i18n="footer.needHelp">Need help now?</h2>
        <a href="tel:1930" data-i18n="footer.call1930">Call 1930 (India cyber fraud helpline)</a>
        <a href="https://cybercrime.gov.in" target="_blank" rel="noopener" data-i18n="footer.report">Report at cybercrime.gov.in</a>
      </div>
    </div>
    <div class="footer-bottom">
      <p>
        <span data-i18n="footer.built">Built by Kritank Jain.</span>
        ${REPO_URL ? `<a href="${REPO_URL}" target="_blank" rel="noopener" data-i18n="footer.source">Source code</a>` : ""}
      </p>
      <p data-i18n="footer.models">Built on Meta Muse Wonder, Muse Spark, Muse Voice Transcribe and SAM 3.1.</p>
      <p class="footer-disclaimer" data-i18n="footer.disclaimer">Sentinel gives safety guidance, not legal or financial advice. If you are in danger, contact your local police.</p>
    </div>`;
}

/* ---------- API ---------- */

async function callApi(url, options) {
  const res = await fetch(url, options);
  let data = {};
  try {
    data = await res.json();
  } catch { /* non-JSON error body */ }
  if (!res.ok) throw new Error(data.detail || t("error.generic"));
  return data;
}

/* ---------- Loading messages ---------- */

function startLoading(box, textEl, keys) {
  let i = 0;
  textEl.textContent = t(keys[0]);
  box.hidden = false;
  const timer = setInterval(() => {
    i = Math.min(i + 1, keys.length - 1);
    textEl.textContent = t(keys[i]);
  }, 3500);
  return () => {
    clearInterval(timer);
    box.hidden = true;
  };
}

/* ---------- Verdict sheet ---------- */

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text != null) node.textContent = text;   // textContent only: scam text is never treated as HTML
  return node;
}

const TOOL_LABELS = { check_url: "tool.link", web_search: "tool.search", "browser.search": "tool.search" };

// opts.media: an element shown under the verdict (e.g. screenshot with evidence boxes)
// opts.extra: an element shown after the warning signs (e.g. voice analysis)
function renderVerdict(container, v, opts = {}) {
  container.replaceChildren();
  const verdict = String(v.verdict || "SAFE").toUpperCase();
  const sheet = el("article", `sheet result verdict-${verdict.toLowerCase()}`);

  const head = el("div", "verdict-head");
  const title = el("h2", "verdict-title", t(`verdict.${verdict}`));
  title.tabIndex = -1;
  head.append(title, el("span", "risk", `${t("label.risk")} ${v.threat_score ?? 0}/100`));
  sheet.append(head);

  if (v.scam_type) sheet.append(el("p", "scam-type", v.scam_type));

  if (v.action) {
    const action = el("div", "action");
    action.append(el("h3", null, t("label.action")), el("p", null, v.action));
    sheet.append(action);
  }

  if (opts.media) sheet.append(opts.media);

  if (v.explanation) {
    sheet.append(el("h3", null, t("label.why")), el("p", "explanation", v.explanation));
  }

  if (v.tactics?.length) {
    sheet.append(el("h3", null, t("label.signs")));
    const list = el("ul", "signs");
    v.tactics.forEach((tac) => {
      const li = el("li");
      li.append(el("strong", null, tac.tactic));
      if (tac.evidence) li.append(el("q", null, tac.evidence));
      list.append(li);
    });
    sheet.append(list);
  }

  if (opts.extra) sheet.append(opts.extra);

  if (v.tool_findings?.length) {
    sheet.append(el("h3", null, t("label.checked")));
    const list = el("ul", "findings");
    v.tool_findings.forEach((f) => {
      const li = el("li");
      li.append(el("span", "tool", t(TOOL_LABELS[f.tool] || "tool.other")), el("span", null, f.finding));
      list.append(li);
    });
    sheet.append(list);
  }

  container.append(sheet);
  title.focus({ preventScroll: true });
  sheet.scrollIntoView({ behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth", block: "start" });
}

/* ---------- Image input: choose, paste or drop ---------- */

function setupImageInput({ dropTarget, fileInput, preview, previewImg, previewName, removeBtn, onError, onChange }) {
  const TYPES = ["image/png", "image/jpeg"];
  let file = null;

  function attach(f) {
    if (!f || !TYPES.includes(f.type)) {
      onError(t("error.imageType"));
      return;
    }
    file = f;
    if (previewImg.src) URL.revokeObjectURL(previewImg.src);
    previewImg.src = URL.createObjectURL(f);
    if (previewName) previewName.textContent = f.name || "screenshot.png";
    preview.hidden = false;
    onChange?.(file);
  }

  function clear() {
    file = null;
    fileInput.value = "";
    if (previewImg.src) URL.revokeObjectURL(previewImg.src);
    previewImg.removeAttribute("src");
    preview.hidden = true;
    onChange?.(null);
  }

  fileInput.addEventListener("change", () => fileInput.files[0] && attach(fileInput.files[0]));
  removeBtn?.addEventListener("click", clear);

  document.addEventListener("paste", (e) => {
    const item = [...(e.clipboardData?.items || [])].find((i) => i.type.startsWith("image/"));
    if (item) {
      e.preventDefault();
      attach(item.getAsFile());
    }
  });

  ["dragenter", "dragover"].forEach((ev) => dropTarget.addEventListener(ev, (e) => {
    e.preventDefault();
    dropTarget.classList.add("dragging");
  }));
  ["dragleave", "drop"].forEach((ev) => dropTarget.addEventListener(ev, () => dropTarget.classList.remove("dragging")));
  dropTarget.addEventListener("drop", (e) => {
    e.preventDefault();
    const f = e.dataTransfer?.files?.[0];
    if (f) attach(f);
  });

  return { get file() { return file; }, clear };
}

/* ---------- Evidence view: numbered boxes over the image + matching list ---------- */

function renderEvidence(imageUrl, evidence) {
  const figure = el("figure", "evidence");
  const frame = el("div", "evidence-frame");
  const img = el("img");
  img.src = imageUrl;
  img.alt = "";
  frame.append(img);

  const list = el("ol", "evidence-list");
  const { width, height, boxes = [] } = evidence || {};

  boxes.forEach((b, i) => {
    const [x1, y1, x2, y2] = b.box;
    const pct = (v, total) => Math.max(0, Math.min(100, (v / total) * 100));
    const box = el("div", "ebox");
    box.style.left = pct(x1, width) + "%";
    box.style.top = pct(y1, height) + "%";
    box.style.width = pct(x2 - x1, width) + "%";
    box.style.height = pct(y2 - y1, height) + "%";
    box.append(el("span", "etag", String(i + 1)));
    frame.append(box);

    const li = el("li");
    li.tabIndex = 0;
    li.append(el("span", "num", String(i + 1)));
    const text = el("span", "etext");
    text.append(el("strong", null, b.label),
                el("small", null, t(b.source === "sam-3.1" ? "source.sam" : "source.wonder")));
    li.append(text);
    const on = () => box.classList.add("active");
    const off = () => box.classList.remove("active");
    li.addEventListener("mouseenter", on);
    li.addEventListener("mouseleave", off);
    li.addEventListener("focus", on);
    li.addEventListener("blur", off);
    list.append(li);
  });

  const side = el("div", "evidence-side");
  if (boxes.length) side.append(el("h3", null, t("label.evidence")), list);
  figure.append(frame, side);
  return figure;
}

/* ---------- Audio: convert anything to 16 kHz mono WAV, record from the mic ---------- */

function encodeWav(samples, rate) {
  const view = new DataView(new ArrayBuffer(44 + samples.length * 2));
  const write = (offset, str) => { for (let i = 0; i < str.length; i++) view.setUint8(offset + i, str.charCodeAt(i)); };
  write(0, "RIFF");
  view.setUint32(4, 36 + samples.length * 2, true);
  write(8, "WAVE");
  write(12, "fmt ");
  view.setUint32(16, 16, true);
  view.setUint16(20, 1, true);              // PCM
  view.setUint16(22, 1, true);              // mono
  view.setUint32(24, rate, true);
  view.setUint32(28, rate * 2, true);
  view.setUint16(32, 2, true);
  view.setUint16(34, 16, true);             // 16-bit
  write(36, "data");
  view.setUint32(40, samples.length * 2, true);
  let offset = 44;
  for (const s of samples) {
    const c = Math.max(-1, Math.min(1, s));
    view.setInt16(offset, c < 0 ? c * 0x8000 : c * 0x7fff, true);
    offset += 2;
  }
  return new Blob([view], { type: "audio/wav" });
}

async function resampleMono(samples, fromRate, toRate) {
  if (fromRate === toRate) return samples;
  const off = new OfflineAudioContext(1, Math.ceil((samples.length * toRate) / fromRate), toRate);
  const buf = off.createBuffer(1, samples.length, fromRate);
  buf.copyToChannel(samples, 0);
  const src = off.createBufferSource();
  src.buffer = buf;
  src.connect(off.destination);
  src.start();
  return (await off.startRendering()).getChannelData(0);
}

// Any audio file the browser can play (MP3, M4A, OGG/Opus, WAV) -> 16 kHz mono WAV.
async function fileToWav(file, maxSeconds = 600) {
  const ctx = new AudioContext();
  let decoded;
  try {
    decoded = await ctx.decodeAudioData(await file.arrayBuffer());
  } catch {
    throw new Error(t("error.audioType"));
  } finally {
    ctx.close();
  }
  if (decoded.duration > maxSeconds) throw new Error(t("error.tooLong"));
  const rate = 16000;
  const off = new OfflineAudioContext(1, Math.ceil(decoded.duration * rate), rate);
  const src = off.createBufferSource();
  src.buffer = decoded;                     // stereo is mixed down to mono automatically
  src.connect(off.destination);
  src.start();
  return encodeWav((await off.startRendering()).getChannelData(0), rate);
}

// Microphone capture. onChunk(Float32Array, sampleRate) is optional (used for live calls).
async function startMic(onChunk) {
  let stream;
  try {
    stream = await navigator.mediaDevices.getUserMedia({
      audio: { channelCount: 1, echoCancellation: true, noiseSuppression: true },
    });
  } catch {
    throw new Error(t("error.mic"));
  }
  const ctx = new AudioContext();
  const source = ctx.createMediaStreamSource(stream);
  const proc = ctx.createScriptProcessor(4096, 1, 1);
  const chunks = [];
  proc.onaudioprocess = (e) => {
    const data = new Float32Array(e.inputBuffer.getChannelData(0));
    chunks.push(data);
    onChunk?.(data, ctx.sampleRate);
  };
  source.connect(proc);
  proc.connect(ctx.destination);           // output stays silent; needed so processing runs

  return {
    sampleRate: ctx.sampleRate,
    async stop() {
      proc.disconnect();
      source.disconnect();
      stream.getTracks().forEach((tr) => tr.stop());
      const rate = ctx.sampleRate;
      await ctx.close();
      const all = new Float32Array(chunks.reduce((n, c) => n + c.length, 0));
      let o = 0;
      for (const c of chunks) { all.set(c, o); o += c.length; }
      return encodeWav(await resampleMono(all, rate, 16000), 16000);
    },
  };
}

/* ---------- Voice analysis + transcript blocks ---------- */

function renderVoiceAnalysis(va) {
  if (!va) return null;
  const verdict = String(va.verdict || "UNCERTAIN").toUpperCase();
  const box = el("div", `voice-box voice-${verdict.toLowerCase()}`);
  box.append(el("h3", null, t("label.voice")), el("p", "voice-verdict", t(`voice.${verdict}`)));

  const pct = Math.max(0, Math.min(100, Number(va.synthetic_likelihood) || 0));
  const meter = el("div", "meter");
  meter.setAttribute("role", "meter");
  meter.setAttribute("aria-valuemin", "0");
  meter.setAttribute("aria-valuemax", "100");
  meter.setAttribute("aria-valuenow", String(pct));
  meter.setAttribute("aria-label", t("voice.likelihood"));
  const fill = el("span");
  fill.style.width = pct + "%";
  meter.append(fill);
  box.append(el("p", "meter-label", `${t("voice.likelihood")}: ${pct}%`), meter);

  if (va.signals?.length) {
    const ul = el("ul", "voice-signals");
    va.signals.forEach((sig) => ul.append(el("li", null, sig)));
    box.append(ul);
  }
  box.append(el("p", "voice-note", t("voice.note")));
  return box;
}

function renderTranscript(v) {
  if (!v.transcript) return null;
  const details = el("details", "transcript");
  details.append(el("summary", null, t("label.transcript")));
  if (v.turns?.length) {
    v.turns.forEach((turn) => {
      const p = el("p");
      p.append(el("strong", null, `${t("speaker")} ${turn.speaker || "A"}: `), document.createTextNode(turn.transcript || ""));
      details.append(p);
    });
  } else {
    details.append(el("p", null, v.transcript));
  }
  return details;
}