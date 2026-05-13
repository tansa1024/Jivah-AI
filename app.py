import os
import streamlit as st
import numpy as np
from PIL import Image
import base64
from io import BytesIO
import requests

st.set_page_config(
    page_title="Jivha AI — Ayurvedic Tongue Analysis",
    layout="wide",
    page_icon="🌿",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# CSS — Exact Figma Match
# ---------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=Inter:wght@300;400;500&display=swap');

/* Hide Streamlit elements */
#MainMenu, footer, header, [data-testid="stHeader"] { visibility: hidden !important; display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }

/* Set body background */
.stApp {
    background-color: #F4F2EC !important;
}

/* Adjust padding so content doesn't overlap fixed navbar/footer */
.block-container {
    padding-top: 150px !important;
    padding-bottom: 150px !important;
    max-width: 100% !important;
}

/* ── Navbar (Fixed, Full Width, White) ── */
.custom-navbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 80px;
    background-color: #FFFFFF;
    border-bottom: 1px solid #EBEBEB;
    display: flex;
    align-items: center;
    padding: 0 60px;
    z-index: 999999;
}
.custom-navbar .logo-circle {
    background-color: #6B8E70;
    color: white;
    width: 38px;
    height: 38px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    font-weight: 500;
    margin-right: 14px;
}
.custom-navbar .logo-text {
    font-family: 'Playfair Display', serif;
    font-size: 24px;
    font-weight: 600;
    color: #2C3530;
}
.custom-navbar .nav-home-link {
    margin-left: auto;
    font-family: 'Inter', sans-serif;
    font-size: 15px;
    font-weight: 500;
    color: #6B8E70;
    text-decoration: none;
    padding: 8px 20px;
    border: 1.5px solid #6B8E70;
    border-radius: 8px;
    transition: background 0.2s, color 0.2s;
    display: none;
}
.custom-navbar .nav-home-link:hover {
    background: #6B8E70;
    color: #ffffff;
    text-decoration: none;
}

/* ── Footer (Fixed, Full Width, White) ── */
.custom-footer {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    height: 120px;
    background-color: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    z-index: 999999;
}
.custom-footer-text {
    color: #9DA39E;
    font-family: 'Inter', sans-serif;
    font-size: 14px;
    line-height: 1.6;
    font-weight: 400;
}

/* Typography for Hero */
.hero-title {
    font-family: 'Playfair Display', serif !important;
    font-size: 56px !important;
    font-weight: 600 !important;
    color: #2A3631 !important;
    text-align: center !important;
    line-height: 1.2 !important;
    margin-bottom: 24px !important;
}
.hero-subtitle {
    font-family: 'Inter', sans-serif !important;
    font-size: 18px !important;
    font-weight: 300 !important;
    color: #6E7570 !important;
    text-align: center !important;
    max-width: 650px !important;
    margin: 0 auto 40px auto !important;
    line-height: 1.6 !important;
}

/* ── Streamlit Button overrides ── */
[data-testid="stButton"] > button {
    background-color: #8DA990 !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 32px !important;
    font-size: 16px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    box-shadow: none !important;
    transition: background 0.2s !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 8px !important;
}
[data-testid="stButton"] > button p {
    margin: 0 !important;
    padding: 0 !important;
}
[data-testid="stButton"] > button:hover {
    background-color: #79957C !important;
}

/* Hero CTA button rendered as HTML */
.hero-cta {
    display: flex;
    justify-content: center;
    margin-top: 10px;
}
.hero-cta a {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    background-color: #8DA990;
    color: #FFFFFF;
    font-family: 'Inter', sans-serif;
    font-size: 16px;
    font-weight: 500;
    padding: 14px 36px;
    border-radius: 10px;
    text-decoration: none;
    cursor: pointer;
    transition: background 0.2s;
    border: none;
}
.hero-cta a:hover {
    background-color: #79957C;
    color: #FFFFFF;
    text-decoration: none;
}

/* Other page elements */
.upload-box {
    border: 2px dashed #8BA58D;
    border-radius: 18px;
    background: #FFFFFF;
    padding: 52px 30px;
    max-width: 620px;
    width: 100%;
    margin: 0 auto 24px;
    text-align: center;
}
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    color: #2A3631;
    text-align: center;
    margin: 10px 0 30px;
}
.white-card {
    background: #FFFFFF;
    border-radius: 20px;
    padding: 28px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.03);
}
div[data-testid="stFileUploader"] section { border: none !important; background: transparent !important; }
</style>

<!-- Inject Fixed Navbar -->
<div class="custom-navbar">
    <div class="logo-circle">जि</div>
    <div class="logo-text">Jivha AI</div>
    <a href="/?go=home" target="_self" class="nav-home-link">← Back to Home</a>
</div>

<!-- Inject Fixed Footer -->
<div class="custom-footer">
    <div class="custom-footer-text">
        Jivha AI combines ancient Ayurvedic wisdom with modern artificial intelligence.<br>
        This tool is for educational purposes and should not replace professional medical advice.
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Constants
# ---------------------------------------------------------
MODEL_PATH = "models/Windows-A-DSLR-DenseNet121-20260512-1409.keras"
# UPDATE THIS WITH YOUR DROPBOX LINK (change dl=0 to dl=1)
DROPBOX_MODEL_URL = "https://www.dropbox.com/scl/fi/gwcgke1tswpqiydeb0k34/Windows-A-DSLR-DenseNet121-20260512-1409.keras?rlkey=9v7b7rt6wxfx5u0ogt1k701ua&st=322knhsh&dl=1"
IMG_SIZE   = (299, 299)
CLASS_LABELS = {0: "Pitta", 1: "Vata", 2: "Kapha"}

DOSHA_META = {
    "Pitta": {
        "icon_svg_white": '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8.5 14.5A2.5 2.5 0 0011 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 11-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 002.5 2.5z"/></svg>',
        "icon_svg_small": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#D9695A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8.5 14.5A2.5 2.5 0 0011 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 11-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 002.5 2.5z"/></svg>',
        "icon_bg": "#D9695A", "element": "Fire & Water", "desc": "Driven, focused, and passionate", "bar_color": "#D9695A"
    },
    "Vata": {
        "icon_svg_white": '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9.59 4.59A2 2 0 1 1 11 8H2m10.59 11.41A2 2 0 1 0 14 16H2m15.73-8.27A2.5 2.5 0 1 1 19.5 12H2"/></svg>',
        "icon_svg_small": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#7A9CB0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9.59 4.59A2 2 0 1 1 11 8H2m10.59 11.41A2 2 0 1 0 14 16H2m15.73-8.27A2.5 2.5 0 1 1 19.5 12H2"/></svg>',
        "icon_bg": "#7A9CB0", "element": "Air & Ether", "desc": "Creative, energetic, and adaptable", "bar_color": "#7A9CB0"
    },
    "Kapha": {
        "icon_svg_white": '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/></svg>',
        "icon_svg_small": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#5C7A5E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/></svg>',
        "icon_bg": "#5C7A5E", "element": "Earth & Water", "desc": "Calm, nurturing, and steady", "bar_color": "#5C7A5E"
    }
}

FOODS = {
    "Pitta": {
        "favor": [
            {"name": "Coconut Water", "desc": "Provides essential hydration and a refreshing cooling effect."},
            {"name": "Cucumber & Mint", "desc": "Refreshing ingredients that can help soothe digestion."},
            {"name": "Sweet Fruits", "desc": "Melons, grapes, pears, and sweet mangoes offer natural energy."},
            {"name": "Leafy Greens", "desc": "Spinach, kale, and lettuce provide essential nutrients without heaviness."},
            {"name": "Light Grains", "desc": "Basmati rice or oats are gentle on the stomach and easy to digest."},
            {"name": "Healthy Fats", "desc": "Moderate amounts of ghee or olive oil provide nourishing healthy fats."},
            {"name": "Gentle Spices", "desc": "Coriander and fennel can aid in comfortable digestion without excess heat."},
        ],
        "avoid": [
            {"name": "Chilies & Hot Spices", "desc": "Can cause acid reflux or digestive discomfort in some individuals."},
            {"name": "Fried & Oily Foods", "desc": "High fat content can slow digestion and feel overly heavy."},
            {"name": "Alcohol & Caffeine", "desc": "Stimulants that can contribute to dehydration and digestive irritation."},
            {"name": "Sour Citrus Fruits", "desc": "Highly acidic fruits might irritate a sensitive stomach."},
            {"name": "Heavy Meats", "desc": "Require more energy to digest and can feel heavy after meals."},
            {"name": "Tomatoes & Vinegar", "desc": "Acidic ingredients that might trigger heartburn if consumed in excess."},
        ]
    },
    "Vata": {
        "favor": [
            {"name": "Warm Soups & Stews", "desc": "Easy to digest and provide comforting, nutrient-dense hydration."},
            {"name": "Root Vegetables", "desc": "Carrots, beets, and sweet potatoes offer steady energy and essential fiber."},
            {"name": "Cooked Grains", "desc": "Warm oats and cooked rice are soothing and gentle on digestion."},
            {"name": "Nutrient-Dense Fruits", "desc": "Ripe bananas and avocados provide sustained energy and healthy fats."},
            {"name": "Warming Spices", "desc": "Mild spices like ginger and cumin can support regular digestion."},
            {"name": "Healthy Oils & Dairy", "desc": "Warm milk or sesame oil can be deeply nourishing and comforting."},
        ],
        "avoid": [
            {"name": "Raw Salads & Cold Foods", "desc": "Can sometimes be harder to digest and may cause bloating."},
            {"name": "Carbonated Drinks", "desc": "The trapped gas can contribute to bloating and digestive discomfort."},
            {"name": "Dry & Brittle Foods", "desc": "Crackers and dried fruits might slow digestion if not paired with liquids."},
            {"name": "Caffeine & Stimulants", "desc": "Can sometimes increase feelings of restlessness or anxiety."},
            {"name": "Undercooked Beans", "desc": "Unless soaked and cooked well, beans and lentils can cause gas."},
            {"name": "Raw Cruciferous Veggies", "desc": "Raw broccoli or cabbage can be tough to digest and may cause bloating."},
        ]
    },
    "Kapha": {
        "favor": [
            {"name": "Warming Spices", "desc": "Ginger, black pepper, turmeric, and cumin help stimulate digestion and warmth."},
            {"name": "Light Grains", "desc": "Barley, millet, and jowar are lighter on the stomach and provide steady energy."},
            {"name": "Leafy Greens & Vegetables", "desc": "Spinach, methi, and bitter gourd add essential fiber and nutrients without heaviness."},
            {"name": "Lentils & Legumes", "desc": "Moong dal, masoor dal, and chickpeas offer good protein while being relatively easy to digest."},
            {"name": "Fruits in Moderation", "desc": "Pomegranate, apple, pear, and berries are refreshing and lower in natural sugars."},
            {"name": "Warm Herbal Drinks", "desc": "Ginger tea, tulsi tea, and green tea provide gentle stimulation and hydration."},
        ],
        "avoid": [
            {"name": "Deep-Fried Foods", "desc": "High fat content can slow down digestion and feel overly heavy."},
            {"name": "Excess Sugar & Sweets", "desc": "Can contribute to lethargy and unwanted weight gain if consumed frequently."},
            {"name": "Processed Foods & Excess Cheese", "desc": "Take longer to digest and may leave you feeling sluggish."},
            {"name": "Excess Refined Flour", "desc": "Maida-heavy foods lack fiber and can cause digestive sluggishness."},
            {"name": "Sugary Cold Drinks", "desc": "Cold temperatures and high sugar can dampen digestive efficiency."},
            {"name": "Very Large Heavy Meals", "desc": "Eating overly large portions can strain digestion and reduce energy levels."},
        ]
    }
}

DOSHA_TRAITS = {
    "Pitta": [
        {
            "name": "Elemental & Functional Basis",
            "desc": "<ul style='margin:0; padding-left:20px; margin-bottom:0;'><li>Dominance of Agni (Fire) with a secondary presence of Jala (Water)</li><li>Responsible for digestion, metabolism, biochemical transformation, and thermoregulation</li><li>Governs energy production, enzymatic activity, and cellular transformation</li></ul>",
            "icon": '<svg viewBox="0 0 24 24" fill="none" stroke="#6B8E70" stroke-width="2"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"></path></svg>'
        },
        {
            "name": "Physical Characteristics",
            "desc": "<ul style='margin:0; padding-left:20px; margin-bottom:0;'><li>Moderate body build with good musculature</li><li>Body constitution reflects heat (uṣṇa), sharpness (tīkṣṇa), and lightness (laghu)</li><li>Neither very lean like Vāta nor heavy like Kapha</li></ul>",
            "icon": '<svg viewBox="0 0 24 24" fill="none" stroke="#6B8E70" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>'
        },
        {
            "name": "Skin & Hair",
            "desc": "<ul style='margin:0; padding-left:20px; margin-bottom:0;'><li>Skin tends to be warm, sensitive, and moderately oily</li><li>Increased sensitivity to heat and sunlight</li><li>Hair may be fine or soft, with a tendency toward early thinning or graying under imbalance</li></ul>",
            "icon": '<svg viewBox="0 0 24 24" fill="none" stroke="#6B8E70" stroke-width="2"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"></path></svg>'
        },
        {
            "name": "Physiological Tendencies",
            "desc": "<ul style='margin:0; padding-left:20px; margin-bottom:0;'><li>Strong and regular appetite</li><li>Efficient digestion and metabolism</li><li>Tendency toward heat-related symptoms when aggravated</li></ul>",
            "icon": '<svg viewBox="0 0 24 24" fill="none" stroke="#6B8E70" stroke-width="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"></path></svg>'
        },
        {
            "name": "Psychological & Behavioral Traits",
            "desc": "<ul style='margin:0; padding-left:20px; margin-bottom:0;'><li>Sharp intellect, clarity of understanding, and decisiveness</li><li>Strong focus and leadership tendencies</li><li>Irritability or impatience may appear under stress or imbalance</li></ul>",
            "icon": '<svg viewBox="0 0 24 24" fill="none" stroke="#6B8E70" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>'
        },
        {
            "name": "General Regulatory Role",
            "desc": "<ul style='margin:0; padding-left:20px; margin-bottom:0;'><li>Acts as the primary transformational and metabolic regulator</li><li>Maintains energy balance, tissue metabolism, and physiological efficiency</li><li>Excess Pitta leads to inflammation, overheating, hypermetabolism, and irritability</li></ul>",
            "icon": '<svg viewBox="0 0 24 24" fill="none" stroke="#6B8E70" stroke-width="2"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>'
        }
    ],
    "Vata": [
        {
            "name": "Elemental & Functional Basis",
            "desc": "<ul style='margin:0; padding-left:20px; margin-bottom:0;'><li>Dominance of Vāyu (Air) and Ākāśa (Space) elements</li><li>Governs movement, communication, transport, and neural activity in the body</li><li>Responsible for initiation and coordination of physiological functions</li></ul>",
            "icon": '<svg viewBox="0 0 24 24" fill="none" stroke="#6B8E70" stroke-width="2"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"></path></svg>'
        },
        {
            "name": "Physical Characteristics",
            "desc": "<ul style='margin:0; padding-left:20px; margin-bottom:0;'><li>Lean body frame with low body mass</li><li>Difficulty in gaining or maintaining weight</li><li>Body proportions may be irregular or non-uniform</li><li>Generally light (laghu) and dry (rukṣa) constitution</li></ul>",
            "icon": '<svg viewBox="0 0 24 24" fill="none" stroke="#6B8E70" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>'
        },
        {
            "name": "Movement & Activity",
            "desc": "<ul style='margin:0; padding-left:20px; margin-bottom:0;'><li>High mobility and quickness in physical actions</li><li>Preference for movement and activity</li><li>Difficulty in remaining still for long periods</li><li>Fast execution of tasks due to cala guṇa (mobility)</li></ul>",
            "icon": '<svg viewBox="0 0 24 24" fill="none" stroke="#6B8E70" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>'
        },
        {
            "name": "Skin & Hair",
            "desc": "<ul style='margin:0; padding-left:20px; margin-bottom:0;'><li>Dry skin tendency</li><li>Reduced unctuousness and lubrication</li><li>Hair tends to be dry and rough rather than oily</li></ul>",
            "icon": '<svg viewBox="0 0 24 24" fill="none" stroke="#6B8E70" stroke-width="2"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"></path></svg>'
        },
        {
            "name": "Physiological Tendencies",
            "desc": "<ul style='margin:0; padding-left:20px; margin-bottom:0;'><li>Variable appetite and digestion</li><li>Irregular hunger and thirst patterns</li><li>Tendency toward variability and inconsistency in bodily functions</li></ul>",
            "icon": '<svg viewBox="0 0 24 24" fill="none" stroke="#6B8E70" stroke-width="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"></path></svg>'
        },
        {
            "name": "Psychological & Behavioral Traits",
            "desc": "<ul style='margin:0; padding-left:20px; margin-bottom:0;'><li>Quick thinking and rapid mental activity</li><li>Creativity and alertness</li><li>Mental instability or variability under stress</li><li>Susceptibility to anxiety-like features when aggravated</li></ul>",
            "icon": '<svg viewBox="0 0 24 24" fill="none" stroke="#6B8E70" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>'
        },
        {
            "name": "General Regulatory Role",
            "desc": "<ul style='margin:0; padding-left:20px; margin-bottom:0;'><li>Acts as the primary regulator that activates and controls other functional systems</li><li>Any imbalance in Vāta leads to system-wide dysregulation due to its coordinating role</li></ul>",
            "icon": '<svg viewBox="0 0 24 24" fill="none" stroke="#6B8E70" stroke-width="2"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>'
        }
    ],
    "Kapha": [
        {
            "name": "Elemental & Functional Basis",
            "desc": "<ul style='margin:0; padding-left:20px; margin-bottom:0;'><li>Dominance of Jala (Water) and Pṛthvī (Earth) elements</li><li>Responsible for structure, cohesion, stability, lubrication, and nourishment of the body</li><li>Plays a key role in maintaining physical integrity and resistance</li></ul>",
            "icon": '<svg viewBox="0 0 24 24" fill="none" stroke="#6B8E70" stroke-width="2"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"></path></svg>'
        },
        {
            "name": "Physical Characteristics",
            "desc": "<ul style='margin:0; padding-left:20px; margin-bottom:0;'><li>Well-developed, sturdy body frame</li><li>Tendency toward higher body mass</li><li>Slower rate of tissue turnover compared to Vāta and Pitta</li><li>Constitution reflects heaviness (guru) and stability (sthira)</li></ul>",
            "icon": '<svg viewBox="0 0 24 24" fill="none" stroke="#6B8E70" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>'
        },
        {
            "name": "Movement & Activity",
            "desc": "<ul style='margin:0; padding-left:20px; margin-bottom:0;'><li>Slow, steady, and deliberate movements</li><li>Less inclination toward rapid or excessive activity</li><li>Sustained endurance rather than speed</li></ul>",
            "icon": '<svg viewBox="0 0 24 24" fill="none" stroke="#6B8E70" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>'
        },
        {
            "name": "Skin & Hair",
            "desc": "<ul style='margin:0; padding-left:20px; margin-bottom:0;'><li>Skin tends to be smooth and well-lubricated</li><li>Better moisture retention compared to Vāta</li><li>Hair generally shows good strength and density</li></ul>",
            "icon": '<svg viewBox="0 0 24 24" fill="none" stroke="#6B8E70" stroke-width="2"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"></path></svg>'
        },
        {
            "name": "Physiological Tendencies",
            "desc": "<ul style='margin:0; padding-left:20px; margin-bottom:0;'><li>Slow but steady metabolism</li><li>Appetite is stable but digestion may be sluggish</li><li>Strong tissue nourishment and storage capacity</li></ul>",
            "icon": '<svg viewBox="0 0 24 24" fill="none" stroke="#6B8E70" stroke-width="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"></path></svg>'
        },
        {
            "name": "Psychological & Behavioral Traits",
            "desc": "<ul style='margin:0; padding-left:20px; margin-bottom:0;'><li>Calm, stable, and tolerant mental disposition</li><li>Emotional steadiness and patience</li><li>Slower cognitive processing but good memory retention</li></ul>",
            "icon": '<svg viewBox="0 0 24 24" fill="none" stroke="#6B8E70" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>'
        },
        {
            "name": "General Regulatory Role",
            "desc": "<ul style='margin:0; padding-left:20px; margin-bottom:0;'><li>Acts as the primary stabilizing and sustaining principle in the body</li><li>Maintains structural integrity, lubrication, and resistance to stress</li><li>Excess Kapha leads to accumulation, stagnation, heaviness, and reduced activity</li></ul>",
            "icon": '<svg viewBox="0 0 24 24" fill="none" stroke="#6B8E70" stroke-width="2"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>'
        }
    ]
}

# ---------------------------------------------------------
# Session State
# ---------------------------------------------------------
for key, default in [("page","home"),("predictions",None),("dosha",None),("uploaded_image",None)]:
    if key not in st.session_state:
        st.session_state[key] = default

def go_home():
    st.session_state.page = "home"
    st.session_state.predictions = None
    st.session_state.dosha = None
    st.session_state.uploaded_image = None

# ---------------------------------------------------------
# Model
# ---------------------------------------------------------
def download_model_from_dropbox():
    """Download model from Dropbox if it doesn't exist locally."""
    os.makedirs("models", exist_ok=True)
    
    if not os.path.exists(MODEL_PATH):
        try:
            st.info("📥 Downloading AI model (first time only, please wait ~3-5 minutes)...")
            response = requests.get(DROPBOX_MODEL_URL, timeout=600, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            
            with open(MODEL_PATH, 'wb') as f:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            progress = downloaded / total_size
                            st.progress(progress)
            st.success("✅ Model downloaded successfully!")
            return True
        except Exception as e:
            st.error(f"❌ Failed to download model: {e}")
            return False
    return True

@st.cache_resource
def load_trained_model():
    if not download_model_from_dropbox():
        return None
    try:
        import tensorflow as tf
        return tf.keras.models.load_model(MODEL_PATH)
    except Exception as e:
        st.error(f"Model load error: {e}")
        return None

def preprocess_image(img: Image.Image):
    from tensorflow.keras.preprocessing.image import img_to_array
    from tensorflow.keras.applications.densenet import preprocess_input
    
    if img.mode != "RGB":
        img = img.convert("RGB")
    img = img.resize(IMG_SIZE)
    arr = img_to_array(img)
    arr = np.expand_dims(arr, axis=0)
    return preprocess_input(arr)

# Donut chart removed as per design

# Check if coming from HTML button click
if st.query_params.get("go") == "upload":
    st.query_params.clear()
    st.session_state.page = "upload"
    st.rerun()

if st.query_params.get("go") == "home":
    st.query_params.clear()
    go_home()
    st.rerun()

# ==============================================================
# PAGE: HOME
# ==============================================================
if st.session_state.page == "home":
    st.markdown("""
    <h1 class="hero-title">Discover Your Dosha<br>Through Your Tongue</h1>
    <p class="hero-subtitle">Ancient Ayurvedic wisdom meets modern AI. Upload a photo of your tongue and receive personalised wellness insights in seconds.</p>
    <div class="hero-cta">
        <a href="?go=upload" target="_self">📷 Start Your Scan</a>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================
# PAGE: UPLOAD
# ==============================================================
elif st.session_state.page == "upload":
    # ── Upload page title ──
    st.markdown("""
    <style>
    /* Hide the global footer on the upload page */
    .custom-footer { display: none !important; }
    /* Show Back to Home link on upload page */
    .custom-navbar .nav-home-link { display: inline-flex !important; align-items: center; }
    </style>
    <div style="text-align:center; padding: 10px 0 28px;">
        <h2 style="font-family:'Playfair Display',serif; font-size:1.9rem; font-weight:600;
                   color:#2A3631; margin:0;">Upload Your Tongue Image</h2>
    </div>
    """, unsafe_allow_html=True)

    # ── Centred upload card (HTML visual shell) ──
    _, col_up, _ = st.columns([1, 2, 1])
    with col_up:
        st.markdown("""
<div style="border: 2px dashed #A8C0AA; border-radius: 20px; background: #FFFFFF; padding: 48px 32px 32px; text-align: center;">
<!-- tongue outline SVG illustration -->
<svg width="90" height="100" viewBox="0 0 90 100" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin-bottom:20px;">
<circle cx="45" cy="30" r="24" stroke="#BFCFBF" stroke-width="2" fill="none"/>
<line x1="45" y1="54" x2="45" y2="68" stroke="#BFCFBF" stroke-width="2"/>
<path d="M34 58 Q34 78 45 82 Q56 78 56 58" stroke="#BFCFBF" stroke-width="2" fill="none" stroke-linecap="round"/>
<path d="M36 42 Q45 50 54 42" stroke="#BFCFBF" stroke-width="2" fill="none" stroke-linecap="round"/>
<line x1="36" y1="28" x2="40" y2="28" stroke="#BFCFBF" stroke-width="2" stroke-linecap="round"/>
<line x1="50" y1="28" x2="54" y2="28" stroke="#BFCFBF" stroke-width="2" stroke-linecap="round"/>
</svg>
<!-- upload icons row -->
<div style="display:flex; justify-content:center; align-items:center; gap:14px; margin-bottom:14px;">
<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#6B8E70" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
<polyline points="17 8 12 3 7 8"/>
<line x1="12" y1="3" x2="12" y2="15"/>
</svg>
<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#6B8E70" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
<path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/>
<circle cx="12" cy="13" r="4"/>
</svg>
</div>
<p style="font-family:'Inter',sans-serif; font-size:1rem; font-weight:600; color:#2A3631; margin:0 0 6px;">Drag &amp; drop or click to upload</p>
<p style="font-family:'Inter',sans-serif; font-size:0.85rem; color:#8A9490; margin:0 0 20px;">Position your tongue within the guide for best results</p>
<!-- privacy badge inside card -->
<div style="display:inline-flex; align-items:center; gap:8px; background:#F4F2EC; border-radius:20px; padding:6px 16px;">
<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#8A9490" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
<circle cx="12" cy="12" r="10"/>
<path d="M12 8v4"/><path d="M12 16h.01"/>
</svg>
<span style="font-family:'Inter',sans-serif; font-size:0.8rem; color:#6B7C73;">Private &amp; Secure &mdash; <span style="color:#6B8E70;">Images deleted after analysis</span></span>
</div>
</div>
""", unsafe_allow_html=True)

        # Actual Streamlit file uploader (hidden label, appears as native drop zone)
        st.markdown("""
        <style>
        /* 1. Make the column itself a relative container */
        [data-testid="column"]:has([data-testid="stFileUploader"]) {
            position: relative !important;
        }
        
        /* 2. Position the Streamlit uploader wrapper absolutely over the column */
        [data-testid="stElementContainer"]:has([data-testid="stFileUploader"]) {
            position: absolute !important;
            top: 0 !important;
            left: 0 !important;
            width: 100% !important;
            height: 100% !important;
            z-index: 999 !important;
            opacity: 0 !important; /* completely invisible */
        }

        /* 3. Force the internal uploader elements to stretch and fill the space */
        [data-testid="stFileUploader"], 
        [data-testid="stFileUploader"] > section {
            width: 100% !important;
            height: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
            display: flex !important;
            align-items: stretch !important;
            justify-content: stretch !important;
            cursor: pointer !important;
        }
        
        [data-testid="stFileUploader"] > section > div {
            width: 100% !important;
            height: 100% !important;
            display: flex !important;
            align-items: stretch !important;
        }
        </style>
        """, unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Choose a tongue image",
            type=["jpg", "jpeg", "png"],
            label_visibility="hidden"
        )

    if uploaded_file:
        with st.spinner("Loading AI model..."):
            model = load_trained_model()
            
        if model:
            with st.spinner("Analysing your tongue…"):
                image = Image.open(uploaded_file)
                preds = model.predict(preprocess_image(image))[0]
                idx   = int(np.argmax(preds))
                dosha = CLASS_LABELS[idx]

        if dosha == "Other":
            st.error("⚠️ No tongue detected. Please upload a clear, well-lit cropped image of your tongue.")
        else:
            st.session_state.predictions    = preds
            st.session_state.dosha          = dosha
            st.session_state.uploaded_image = image
            st.session_state.page           = "results"
            st.rerun()

# ==============================================================
# PAGE: RESULTS
# ==============================================================
elif st.session_state.page == "results":
    preds  = st.session_state.predictions
    dosha  = st.session_state.dosha
    image  = st.session_state.uploaded_image
    meta   = DOSHA_META[dosha]

    st.markdown("""
    <style>
    /* Hide the global footer on the results page as well for a cleaner look */
    .custom-footer { display: none !important; }
    /* Show Back to Home link on results page */
    .custom-navbar .nav-home-link { display: inline-flex !important; align-items: center; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Your Ayurvedic Analysis</div>', unsafe_allow_html=True)

    # ── Section 1: Dosha Profile & Tongue ──
    col_l, col_r = st.columns(2, gap="large")

    with col_l:
        img_html = ""
        if image:
            buffered = BytesIO()
            # Convert to RGB just in case, or save as PNG. Saving as PNG is safer for RGBA.
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            img_html = f'<img src="data:image/png;base64,{img_str}" style="width:100%; border-radius:12px; object-fit:cover; max-height:400px; margin-top:10px;">'
        
        st.markdown(f'''
        <div class="white-card">
            <div style="font-family:'Playfair Display',serif; font-size:1.3rem; color:#2A3631; margin-bottom:20px;">Tongue Analysis</div>
            {img_html}
        </div>
        ''', unsafe_allow_html=True)

    with col_r:
        # Build progress bars HTML first using safe single-line strings
        bars_html = ""
        for i in range(3):
            lbl   = CLASS_LABELS[i]
            pct   = int(preds[i] * 100)
            color = DOSHA_META[lbl]["bar_color"]
            icon  = DOSHA_META[lbl]["icon_svg_small"]
            bars_html += (
                f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">'
                f'<div style="display:flex;align-items:center;gap:8px;font-family:Inter,sans-serif;font-size:0.95rem;color:#444;">'
                f'<div style="width:18px;height:18px;">{icon}</div> {lbl}</div>'
                f'<div style="font-family:Inter,sans-serif;font-size:0.9rem;color:#666;">{pct}%</div></div>'
                f'<div style="background:#EBE6DF;border-radius:6px;height:12px;margin-bottom:22px;">'
                f'<div style="height:12px;border-radius:6px;width:{pct}%;background:{color};"></div></div>'
            )

        dosha_card = (
            '<div class="white-card">'
            '<div style="font-family:\'Playfair Display\',serif;font-size:1.3rem;color:#2A3631;margin-bottom:20px;">Your Dosha Profile</div>'
            f'<div style="background:#DDE5DA;border-radius:12px;padding:32px 20px;text-align:center;margin-bottom:30px;">'
            f'<div style="width:68px;height:68px;border-radius:50%;background:{meta["icon_bg"]};display:flex;align-items:center;justify-content:center;margin:0 auto 16px;">'
            f'{meta["icon_svg_white"]}</div>'
            f'<div style="font-family:\'Playfair Display\',serif;font-size:1.35rem;color:#2A3631;margin-bottom:6px;">Dominant: {dosha}</div>'
            f'<div style="font-family:Inter,sans-serif;font-size:0.95rem;color:#555;margin-bottom:8px;">{meta["element"]}</div>'
            f'<div style="font-family:Inter,sans-serif;font-size:1rem;color:#2A3631;">{meta["desc"]}</div>'
            '</div>'
            + bars_html +
            '</div>'
        )
        st.markdown(dosha_card, unsafe_allow_html=True)

    # ── Section 2: Dietary Recommendations ──
    st.markdown(f'<div class="section-title" style="margin-top:60px; margin-bottom:40px;">Dietary Recommendations for {dosha}</div>', unsafe_allow_html=True)
    
    col_fav, col_avoid = st.columns(2, gap="large")
    with col_fav:
        st.markdown("""
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:24px;">
            <div style="width:36px; height:36px; background:#8DA990; border-radius:50%; display:flex; align-items:center; justify-content:center;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
            </div>
            <div style="font-family:'Playfair Display',serif; font-size:1.4rem; color:#2A3631;">Foods to Favor</div>
        </div>
        """, unsafe_allow_html=True)
        for item in FOODS[dosha]["favor"]:
            st.markdown(f"""
<div class="white-card" style="padding:12px 18px; margin-bottom:8px; border-radius:10px;">
    <div style="font-family:'Inter',sans-serif; font-size:0.95rem; font-weight:500; color:#2A3631; margin-bottom:3px;">{item['name']}</div>
    <div style="font-family:'Inter',sans-serif; font-size:0.8rem; color:#8A9490;">{item['desc']}</div>
</div>
            """, unsafe_allow_html=True)

    with col_avoid:
        st.markdown("""
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:24px;">
            <div style="width:36px; height:36px; background:#D9695A; border-radius:50%; display:flex; align-items:center; justify-content:center;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
            </div>
            <div style="font-family:'Playfair Display',serif; font-size:1.4rem; color:#2A3631;">Foods to Avoid</div>
        </div>
        """, unsafe_allow_html=True)
        for item in FOODS[dosha]["avoid"]:
            st.markdown(f"""
<div class="white-card" style="padding:12px 18px; margin-bottom:8px; border-radius:10px;">
    <div style="font-family:'Inter',sans-serif; font-size:0.95rem; font-weight:500; color:#2A3631; margin-bottom:3px;">{item['name']}</div>
    <div style="font-family:'Inter',sans-serif; font-size:0.8rem; color:#8A9490;">{item['desc']}</div>
</div>
            """, unsafe_allow_html=True)

    st.markdown('<div style="text-align:center; font-family:\'Inter\',sans-serif; color:#777; font-size:0.9rem; margin-top:30px; margin-bottom:10px; font-style:italic;">*Ayurvedic dietary practices are individualized and should complement modern nutrition and medical advice.</div>', unsafe_allow_html=True)

    # ── Section 3: Dosha Attributes ──
    st.markdown(f'<div class="section-title" style="margin-top:70px; margin-bottom:10px;">Attributes of {dosha}</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center; font-family:\'Inter\',sans-serif; color:#777; font-size:1.05rem; margin-bottom:40px;">Understand your unique physical, mental, and emotional characteristics</div>', unsafe_allow_html=True)

    st.markdown("""
    <style>
    details.dosha-attr {
        background: #F6F5F2;
        border-radius: 10px;
        margin-bottom: 8px;
        overflow: hidden;
        border: 1px solid transparent;
        transition: border 0.2s;
    }
    details.dosha-attr:hover {
        border: 1px solid #EBEBEB;
    }
    details.dosha-attr summary {
        padding: 12px 16px;
        display: flex;
        align-items: center;
        gap: 14px;
        cursor: pointer;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        color: #2A3631;
        font-size: 0.95rem;
        list-style: none;
    }
    details.dosha-attr summary::-webkit-details-marker {
        display: none;
    }
    details.dosha-attr summary .icon-box {
        width: 36px; height: 36px; background: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0;
    }
    details.dosha-attr summary .arrow {
        margin-left: auto;
        transition: transform 0.2s ease-in-out;
    }
    details.dosha-attr[open] summary .arrow {
        transform: rotate(180deg);
    }
    details.dosha-attr .content {
        padding: 0 16px 16px 66px;
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        color: #6E7570;
        line-height: 1.5;
        animation: slideDown 0.3s ease-out;
    }
    @keyframes slideDown {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """, unsafe_allow_html=True)

    _, col_attrs, _ = st.columns([1, 2, 1])
    with col_attrs:
        html_attrs = '<div class="white-card" style="padding:24px;">\n'
        for attr in DOSHA_TRAITS.get(dosha, []):
            html_attrs += f"""<details class="dosha-attr">
<summary>
<div class="icon-box">
<div style="width:20px; height:20px;">{attr['icon']}</div>
</div>
{attr['name']}
<svg class="arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#6B8E70" stroke-width="2"><polyline points="6 9 12 15 18 9"></polyline></svg>
</summary>
<div class="content">{attr['desc']}</div>
</details>
"""
        html_attrs += '</div>'
        st.markdown(html_attrs, unsafe_allow_html=True)
