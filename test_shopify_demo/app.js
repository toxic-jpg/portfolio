// Shopify Section Builder - Vanilla JS Demo
// Demonstrates: section schema, live settings, Liquid-like templating

const SECTIONS = {
  announcement: {
    label: "Announcement Bar",
    schema: {
      text: { type: "text", label: "Message", default: "Free shipping on orders over $50!" },
      link: { type: "text", label: "Link URL (optional)", default: "" },
      bgColor: { type: "color", label: "Background", default: "#00d4aa" },
      textColor: { type: "color", label: "Text Color", default: "#000000" },
      dismissible: { type: "checkbox", label: "Dismissible", default: true }
    },
    render(settings) {
      const bar = document.createElement("div");
      bar.className = "announcement-bar" + (settings.dismissible ? " dismissible" : "");
      bar.style.background = settings.bgColor;
      bar.style.color = settings.textColor;
      if (settings.link) {
        const a = document.createElement("a");
        a.href = settings.link;
        a.style.color = "inherit";
        a.textContent = settings.text;
        bar.appendChild(a);
      } else {
        bar.textContent = settings.text;
      }
      if (settings.dismissible) {
        bar.onclick = () => bar.style.display = "none";
        bar.title = "Click to dismiss";
      }
      return bar;
    }
  },
  features: {
    label: "Feature Grid",
    schema: {
      columns: { type: "select", label: "Columns", options: ["3", "4"], default: "3" },
      card1_icon: { type: "text", label: "Card 1 Icon", default: "🚀" },
      card1_title: { type: "text", label: "Card 1 Title", default: "Fast Shipping" },
      card1_desc: { type: "textarea", label: "Card 1 Description", default: "Delivered to your door in 2-3 business days." },
      card1_btn: { type: "text", label: "Card 1 Button", default: "Shop Now" },
      card2_icon: { type: "text", label: "Card 2 Icon", default: "🔒" },
      card2_title: { type: "text", label: "Card 2 Title", default: "Secure Checkout" },
      card2_desc: { type: "textarea", label: "Card 2 Description", default: "Bank-grade encryption for every transaction." },
      card2_btn: { type: "text", label: "Card 2 Button", default: "Learn More" },
      card3_icon: { type: "text", label: "Card 3 Icon", default: "🔄" },
      card3_title: { type: "text", label: "Card 3 Title", default: "Easy Returns" },
      card3_desc: { type: "textarea", label: "Card 3 Description", default: "30-day hassle-free return policy." },
      card3_btn: { type: "text", label: "Card 3 Button", default: "Policy" },
      card4_icon: { type: "text", label: "Card 4 Icon", default: "💬" },
      card4_title: { type: "text", label: "Card 4 Title", default: "24/7 Support" },
      card4_desc: { type: "textarea", label: "Card 4 Description", default: "Our team is here to help anytime." },
      card4_btn: { type: "text", label: "Card 4 Button", default: "Contact" }
    },
    render(settings) {
      const section = document.createElement("div");
      section.innerHTML = `<h3>Feature Grid</h3><div class="feature-grid" style="grid-template-columns: repeat(${settings.columns}, 1fr);"></div>`;
      const grid = section.querySelector(".feature-grid");
      for (let i = 1; i <= parseInt(settings.columns); i++) {
        const card = document.createElement("div");
        card.className = "feature-card";
        card.innerHTML = `
          <div class="feature-icon">${settings[`card${i}_icon`]}</div>
          <h4>${settings[`card${i}_title`]}</h4>
          <p>${settings[`card${i}_desc`]}</p>
          <button>${settings[`card${i}_btn`]}</button>
        `;
        grid.appendChild(card);
      }
      return section;
    }
  },
  testimonials: {
    label: "Testimonial Carousel",
    schema: {
      autoRotate: { type: "checkbox", label: "Auto-rotate", default: true },
      interval: { type: "number", label: "Interval (ms)", default: 4000 },
      t1_quote: { type: "textarea", label: "Testimonial 1", default: ""This theme saved us weeks of dev work. The sections are incredibly flexible."" },
      t1_author: { type: "text", label: "Author 1", default: "— Sarah M., Founder" },
      t2_quote: { type: "textarea", label: "Testimonial 2", default: ""Best Shopify developer I've worked with. Clean code, fast communication."" },
      t2_author: { type: "text", label: "Author 2", default: "— James K., E-comm Manager" },
      t3_quote: { type: "textarea", label: "Testimonial 3", default: ""The section builder alone is worth 10x the price. Client loves it."" },
      t3_author: { type: "text", label: "Author 3", default: "— Priya R., Agency Owner" }
    },
    render(settings) {
      const section = document.createElement("div");
      section.innerHTML = `<h3>Testimonial Carousel</div><div class="testimonial-carousel"><div class="testimonial-track"></div><div class="carousel-dots"></div></div>`;
      const track = section.querySelector(".testimonial-track");
      const dots = section.querySelector(".carousel-dots");
      const testimonials = [
        { quote: settings.t1_quote, author: settings.t1_author },
        { quote: settings.t2_quote, author: settings.t2_author },
        { quote: settings.t3_quote, author: settings.t3_author }
      ];
      testimonials.forEach((t, i) => {
        const card = document.createElement("div");
        card.className = "testimonial";
        card.innerHTML = `<p>${t.quote}</p><cite>${t.author}</cite>`;
        track.appendChild(card);
        const dot = document.createElement("button");
        dot.dataset.index = i;
        dot.className = i === 0 ? "active" : "";
        dots.appendChild(dot);
      });
      let current = 0;
      const show = (idx) => {
        track.style.transform = `translateX(-${idx * 316}px)`;
        dots.querySelectorAll("button").forEach((d, i) => d.classList.toggle("active", i === idx));
        current = idx;
      };
      dots.addEventListener("click", e => { if (e.target.tagName === "BUTTON") show(+e.target.dataset.index); });
      if (settings.autoRotate) {
        setInterval(() => show((current + 1) % testimonials.length), settings.interval);
      }
      return section;
    }
  }
};

function createInput(schema, key, value, onChange) {
  const group = document.createElement("div");
  group.className = "setting-group";
  const label = document.createElement("label");
  label.textContent = schema.label;
  group.appendChild(label);
  let input;
  switch (schema.type) {
    case "text":
      input = document.createElement("input");
      input.type = "text";
      input.value = value;
      input.oninput = e => onChange(key, e.target.value);
      break;
    case "textarea":
      input = document.createElement("textarea");
      input.value = value;
      input.rows = 2;
      input.oninput = e => onChange(key, e.target.value);
      break;
    case "color":
      input = document.createElement("input");
      input.type = "color";
      input.value = value;
      input.oninput = e => onChange(key, e.target.value);
      break;
    case "checkbox":
      group.className = "setting-group toggle";
      input = document.createElement("input");
      input.type = "checkbox";
      input.checked = value;
      input.onchange = e => onChange(key, e.target.checked);
      group.insertBefore(input, label);
      break;
    case "select":
      input = document.createElement("select");
      schema.options.forEach(opt => {
        const o = document.createElement("option");
        o.value = opt;
        o.textContent = opt;
        input.appendChild(o);
      });
      input.value = value;
      input.onchange = e => onChange(key, e.target.value);
      break;
    case "number":
      input = document.createElement("input");
      input.type = "number";
      input.value = value;
      input.oninput = e => onChange(key, parseInt(e.target.value));
      break;
  }
  if (input) group.appendChild(input);
  return group;
}

function buildSettingsPanel() {
  const form = document.getElementById("settings-form");
  form.innerHTML = "";
  Object.entries(SECTIONS).forEach(([key, sec]) => {
    const fieldset = document.createElement("fieldset");
    fieldset.style.marginBottom = "1.5rem";
    fieldset.innerHTML = `<legend style="color:var(--accent);font-size:0.85rem;margin-bottom:0.5rem">${sec.label}</legend>`;
    Object.entries(sec.schema).forEach(([skey, schema]) => {
      const defaultVal = schema.default;
      const input = createInput(schema, `${key}.${skey}`, defaultVal, updateSetting);
      fieldset.appendChild(input);
    });
    form.appendChild(fieldset);
  });
}

const state = {};
function updateSetting(path, value) {
  const [section, key] = path.split(".");
  if (!state[section]) state[section] = {};
  state[section][key] = value;
  renderPreview();
}

function renderPreview() {
  const preview = document.getElementById("preview");
  preview.innerHTML = "";
  Object.entries(SECTIONS).forEach(([key, sec]) => {
    const settings = { ...sec.schema };
    Object.keys(settings).forEach(k => settings[k] = state[key]?.[k] ?? settings[k].default);
    const rendered = sec.render(settings);
    const wrapper = document.createElement("section");
    wrapper.className = "section";
    wrapper.setAttribute("data-section", key);
    wrapper.appendChild(rendered);
    preview.appendChild(wrapper);
  });
}

buildSettingsPanel();
renderPreview();
console.log("Shopify Section Builder loaded. Edit settings in left panel.");