import os
os.environ['STREAMLIT_SERVER_PORT'] = '8502'

import streamlit as st
import webbrowser
import datetime
import urllib.parse
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import st_folium
import time
import psutil
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import subprocess
import sys
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import json
import io
import base64

# Install required packages if not available
def install_package(package):
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Try to install optional packages
try:
    from googlesearch import search
except ImportError:
    st.warning("googlesearch-python not installed. Google search feature may not work.")
    search = None

try:
    import twilio
    from twilio.rest import Client
except ImportError:
    st.warning("Twilio not installed. SMS/Call features require manual installation.")
    twilio = None

st.set_page_config(page_title="Advanced Multitask Hub", layout="wide")

# Initialize session state for card visibility
if 'active_card' not in st.session_state:
    st.session_state.active_card = None

# Professional Black Theme with Clean Card Design
st.markdown("""
    <style>
    .stApp {
        background-color: #000000;
        color: white;
        font-family: 'Segoe UI', sans-serif;
    }

    h1, h2, h3 {
        color: #ffffff !important;
    }

    .stTextInput>div>div>input,
    .stTextArea>div>textarea,
    .stSelectbox>div>div>div {
        background-color: rgba(255, 255, 255, 0.1);
        color: white !important;
        border: 1px solid #555;
        border-radius: 8px;
    }

    .stButton>button {
        background: linear-gradient(135deg, #1f2937, #4b5563);
        color: white !important;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.2);
        transition: all 0.3s ease;
        width: 100%;
        border: none;
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, #4b5563, #6b7280);
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.4);
        transform: translateY(-2px);
    }

    .tool-card {
        background: rgba(31, 31, 31, 0.95);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        text-align: center;
        min-height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    .tool-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0, 255, 255, 0.2);
        border-color: rgba(0, 255, 255, 0.3);
    }

    .tool-logo {
        font-size: 3rem;
        margin-bottom: 0.5rem;
        filter: drop-shadow(0 0 10px rgba(0, 255, 255, 0.3));
    }

    .tool-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #00ffff;
        margin-bottom: 0.3rem;
    }

    .tool-description {
        color: #cccccc;
        font-size: 0.8rem;
        line-height: 1.3;
    }

    .active-card {
        background: rgba(0, 255, 255, 0.1);
        border: 2px solid rgba(0, 255, 255, 0.4);
        transform: scale(1.02);
    }

    .function-panel {
        background: rgba(20, 20, 20, 0.95);
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        border: 1px solid rgba(0, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 255, 255, 0.1);
    }

    .function-header {
        color: #00ffff;
        font-size: 1.8rem;
        font-weight: bold;
        margin-bottom: 1.5rem;
        text-align: center;
        border-bottom: 2px solid rgba(0, 255, 255, 0.3);
        padding-bottom: 1rem;
    }

    .success-message {
        background: rgba(0, 255, 0, 0.1);
        border: 1px solid rgba(0, 255, 0, 0.3);
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        color: #00ff00;
    }

    .error-message {
        background: rgba(255, 0, 0, 0.1);
        border: 1px solid rgba(255, 0, 0, 0.3);
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        color: #ff6b6b;
    }

    .info-box {
        background: rgba(0, 100, 255, 0.1);
        border: 1px solid rgba(0, 100, 255, 0.3);
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        color: #66b3ff;
    }

    .code-box {
        background: rgba(40, 40, 40, 0.9);
        border: 1px solid #555;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        font-family: 'Courier New', monospace;
        color: #00ff00;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div style="text-align: center; padding: 2rem 0; margin-bottom: 2rem;">
        <h1 style="font-size: 3.5rem; background: linear-gradient(135deg, #00ffff, #ffffff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            🚀 Advanced Multitask Hub
        </h1>
        <p style="font-size: 1.3rem; color: #cccccc; margin-top: 0.5rem;">
            Complete Professional Toolkit - Click on any tool to get started
        </p>
    </div>
""", unsafe_allow_html=True)

# Tool Cards Grid
st.markdown("## 🛠️ Available Tools")

# First Row - Original Tools
col1, col2, col3 = st.columns(3)

# WhatsApp Card
with col1:
    card_class = "tool-card active-card" if st.session_state.active_card == "whatsapp" else "tool-card"
    st.markdown(f"""
        <div class="{card_class}">
            <div class="tool-logo">📱</div>
            <div class="tool-title">WhatsApp</div>
            <div class="tool-description">Send messages to any number worldwide</div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("📱 WhatsApp Tool", key="whatsapp_btn", use_container_width=True):
        st.session_state.active_card = "whatsapp"
        st.rerun()

# Email Card
with col2:
    card_class = "tool-card active-card" if st.session_state.active_card == "email" else "tool-card"
    st.markdown(f"""
        <div class="{card_class}">
            <div class="tool-logo">📧</div>
            <div class="tool-title">Email Sender</div>
            <div class="tool-description">Send professional emails with Gmail</div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("📧 Email Tool", key="email_btn", use_container_width=True):
        st.session_state.active_card = "email"
        st.rerun()

# Maps Card
with col3:
    card_class = "tool-card active-card" if st.session_state.active_card == "maps" else "tool-card"
    st.markdown(f"""
        <div class="{card_class}">
            <div class="tool-logo">🗺️</div>
            <div class="tool-title">Maps & Routes</div>
            <div class="tool-description">Interactive maps and navigation</div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🗺️ Maps Tool", key="maps_btn", use_container_width=True):
        st.session_state.active_card = "maps"
        st.rerun()

# Second Row - System Tools
col4, col5, col6 = st.columns(3)

# System Monitor Card
with col4:
    card_class = "tool-card active-card" if st.session_state.active_card == "system" else "tool-card"
    st.markdown(f"""
        <div class="{card_class}">
            <div class="tool-logo">💻</div>
            <div class="tool-title">System Monitor</div>
            <div class="tool-description">Check RAM, CPU, and system info</div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("💻 System Tool", key="system_btn", use_container_width=True):
        st.session_state.active_card = "system"
        st.rerun()

# SMS & Call Card
with col5:
    card_class = "tool-card active-card" if st.session_state.active_card == "sms" else "tool-card"
    st.markdown(f"""
        <div class="{card_class}">
            <div class="tool-logo">📞</div>
            <div class="tool-title">SMS & Calls</div>
            <div class="tool-description">Send SMS and make calls</div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("📞 SMS/Call Tool", key="sms_btn", use_container_width=True):
        st.session_state.active_card = "sms"
        st.rerun()

# Web Tools Card
with col6:
    card_class = "tool-card active-card" if st.session_state.active_card == "web" else "tool-card"
    st.markdown(f"""
        <div class="{card_class}">
            <div class="tool-logo">🌐</div>
            <div class="tool-title">Web Tools</div>
            <div class="tool-description">Google search & web scraping</div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🌐 Web Tools", key="web_btn", use_container_width=True):
        st.session_state.active_card = "web"
        st.rerun()

# Third Row - Advanced Tools
col7, col8, col9 = st.columns(3)

# Programming Tools Card
with col7:
    card_class = "tool-card active-card" if st.session_state.active_card == "programming" else "tool-card"
    st.markdown(f"""
        <div class="{card_class}">
            <div class="tool-logo">🐍</div>
            <div class="tool-title">Programming</div>
            <div class="tool-description">Python concepts & tutorials</div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🐍 Programming", key="programming_btn", use_container_width=True):
        st.session_state.active_card = "programming"
        st.rerun()

# Image Tools Card
with col8:
    card_class = "tool-card active-card" if st.session_state.active_card == "image" else "tool-card"
    st.markdown(f"""
        <div class="{card_class}">
            <div class="tool-logo">🖼️</div>
            <div class="tool-title">Image Tools</div>
            <div class="tool-description">Create & edit digital images</div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🖼️ Image Tools", key="image_btn", use_container_width=True):
        st.session_state.active_card = "image"
        st.rerun()

# AI Tools Card
with col9:
    card_class = "tool-card active-card" if st.session_state.active_card == "ai" else "tool-card"
    st.markdown(f"""
        <div class="{card_class}">
            <div class="tool-logo">🤖</div>
            <div class="tool-title">AI Comparison</div>
            <div class="tool-description">Compare AI models & performance</div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🤖 AI Tools", key="ai_btn", use_container_width=True):
        st.session_state.active_card = "ai"
        st.rerun()

# Show active tool panel
if st.session_state.active_card:
    st.markdown("---")
    
    # Close button at the top
    if st.button("❌ Close Tool", key="close_tool", use_container_width=False):
        st.session_state.active_card = None
        st.rerun()
    
    # WhatsApp Function Panel
    if st.session_state.active_card == "whatsapp":
        st.markdown("""
            <div class="function-panel">
                <div class="function-header">📱 WhatsApp Messenger</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📱 Send WhatsApp Message (No Contact Required)")
        
        col_w1, col_w2 = st.columns([3, 1])
        with col_w1:
            number = st.text_input("📞 Phone Number (with country code)", 
                                 placeholder="Example: +919876543210", 
                                 help="Include country code like +91 for India, +1 for USA")
            message = st.text_area("💬 Message", 
                                 placeholder="Type your message here...", 
                                 height=100)
        
        with col_w2:
            st.markdown("### 💡 Tips")
            st.info("• Include country code\n• No contact saving needed\n• Works globally\n• Opens WhatsApp Web")
        
        if st.button("🚀 Send WhatsApp Message", key="send_whatsapp", use_container_width=True):
            if number and message:
                try:
                    # Clean the number
                    clean_number = number.replace("+", "").replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
                    encoded_message = urllib.parse.quote(message)
                    
                    # Create WhatsApp URL
                    whatsapp_url = f"https://wa.me/{clean_number}?text={encoded_message}"
                    
                    # Show the URL and try to open it
                    st.markdown(f"""
                        <div class="success-message">
                            ✅ WhatsApp link created! Click the link below:
                            <br><br>
                            <a href="{whatsapp_url}" target="_blank" style="color: #00ffff; text-decoration: underline;">
                                🔗 Open WhatsApp Message
                            </a>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.code(whatsapp_url, language="text")
                    
                    # Try to open automatically
                    try:
                        webbrowser.open(whatsapp_url)
                    except:
                        pass
                        
                except Exception as e:
                    st.error(f"❌ Error creating WhatsApp link: {str(e)}")
            else:
                st.warning("⚠️ Please fill in both phone number and message.")
    
    # Email Function Panel - CORRECTED VERSION
    elif st.session_state.active_card == "email":
        st.markdown("""
            <div class="function-panel">
                <div class="function-header">📧 Professional Email Sender</div>
            </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["📧 Gmail SMTP", "📮 Quick Email", "ℹ️ Setup Guide"])
        
        with tab1:
            st.markdown("### 📧 Send Email via Gmail SMTP")
            
            col_e1, col_e2 = st.columns([3, 1])
            with col_e1:
                # Gmail SMTP Configuration
                st.markdown("#### 🔐 Gmail Configuration")
                sender_email = st.text_input("📧 Your Gmail Address", 
                                           placeholder="youremail@gmail.com",
                                           help="Your Gmail email address")
                sender_password = st.text_input("🔑 App Password", 
                                              type="password",
                                              help="Gmail App Password (NOT your regular password)")
                
                st.markdown("#### 📝 Email Details")
                recipient_email = st.text_input("📮 Recipient Email", 
                                               placeholder="recipient@example.com")
                email_subject = st.text_input("📝 Subject", 
                                            placeholder="Email subject")
                email_body = st.text_area("✉️ Email Body", 
                                        placeholder="Write your email content here...", 
                                        height=150)
                
                # Email format options
                email_format = st.selectbox("📄 Email Format", ["Plain Text", "HTML"])
                
                if email_format == "HTML":
                    st.info("💡 You can use HTML tags like <b>bold</b>, <i>italic</i>, <br> for line breaks, etc.")
                
                if st.button("📤 Send Email", key="send_gmail", use_container_width=True):
                    if all([sender_email, sender_password, recipient_email, email_subject, email_body]):
                        try:
                            with st.spinner("📤 Sending email..."):
                                # Create message
                                msg = MIMEMultipart()
                                msg['From'] = sender_email
                                msg['To'] = recipient_email
                                msg['Subject'] = email_subject
                                
                                # Add body to email
                                if email_format == "HTML":
                                    msg.attach(MIMEText(email_body, 'html'))
                                else:
                                    msg.attach(MIMEText(email_body, 'plain'))
                                
                                # Gmail SMTP configuration
                                server = smtplib.SMTP('smtp.gmail.com', 587)
                                server.starttls()  # Enable security
                                server.login(sender_email, sender_password)
                                
                                # Send email
                                text = msg.as_string()
                                server.sendmail(sender_email, recipient_email, text)
                                server.quit()
                                
                                st.success("✅ Email sent successfully!")
                                st.balloons()
                                
                        except smtplib.SMTPAuthenticationError:
                            st.error("❌ Authentication failed! Please check your email and app password.")
                            st.info("💡 Make sure you're using an App Password, not your regular Gmail password!")
                        except smtplib.SMTPRecipientsRefused:
                            st.error("❌ Recipient email address rejected. Please check the email address.")
                        except smtplib.SMTPConnectError:
                            st.error("❌ Failed to connect to Gmail SMTP server. Check your internet connection.")
                        except smtplib.SMTPServerDisconnected:
                            st.error("❌ SMTP server disconnected unexpectedly. Please try again.")
                        except Exception as e:
                            st.error(f"❌ Error sending email: {str(e)}")
                            st.info("💡 Check the Setup Guide tab for help with Gmail configuration.")
                    else:
                        st.warning("⚠️ Please fill in all required fields.")
            
            with col_e2:
                st.markdown("### 📧 Email Info")
                st.info("• Uses Gmail SMTP server\n• Requires App Password\n• Supports HTML emails\n• Professional delivery\n• Works with any recipient")
                
                st.markdown("### 📊 Email Status")
                if 'email_sent_count' not in st.session_state:
                    st.session_state.email_sent_count = 0
                st.metric("Emails Sent Today", st.session_state.email_sent_count)
        
        with tab2:
            st.markdown("### 📮 Quick Email (Default Client)")
            
            col_q1, col_q2 = st.columns([3, 1])
            with col_q1:
                quick_recipient = st.text_input("📮 Recipient Email", 
                                              placeholder="recipient@example.com", 
                                              key="quick_recipient")
                quick_subject = st.text_input("📝 Subject", 
                                            placeholder="Email subject", 
                                            key="quick_subject")
                quick_body = st.text_area("✉️ Email Body", 
                                        placeholder="Write your email content here...", 
                                        height=120, 
                                        key="quick_body")
                
                if st.button("📤 Open Email Client", key="open_email_client", use_container_width=True):
                    if quick_recipient and quick_subject and quick_body:
                        try:
                            # Create mailto URL
                            mailto_url = f"mailto:{quick_recipient}?subject={urllib.parse.quote(quick_subject)}&body={urllib.parse.quote(quick_body)}"
                            
                            st.markdown(f"""
                                <div class="success-message">
                                    ✅ Email link created! Click the link below:
                                    <br><br>
                                    <a href="{mailto_url}" target="_blank" style="color: #00ffff; text-decoration: underline;">
                                        🔗 Open Email Client
                                    </a>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            try:
                                webbrowser.open(mailto_url)
                            except:
                                pass
                                
                        except Exception as e:
                            st.error(f"❌ Error creating email link: {str(e)}")
                    else:
                        st.warning("⚠️ Please fill in all fields.")
            
            with col_q2:
                st.markdown("### 📧 Quick Info")
                st.info("• Opens default email app\n• Works with Outlook, Apple Mail\n• No configuration needed\n• Quick and simple")
        
        with tab3:
            st.markdown("### ℹ️ Gmail App Password Setup Guide")
            
            st.markdown("""
                <div class="info-box">
                    <h4>🔐 How to Create Gmail App Password</h4>
                    <p><strong>Step 1:</strong> Go to your <a href="https://myaccount.google.com" target="_blank">Google Account</a></p>
                    <p><strong>Step 2:</strong> Click on "Security" in the left sidebar</p>
                    <p><strong>Step 3:</strong> Enable "2-Step Verification" if not already enabled</p>
                    <p><strong>Step 4:</strong> Scroll down and click "App passwords"</p>
                    <p><strong>Step 5:</strong> Select "Mail" and your device</p>
                    <p><strong>Step 6:</strong> Copy the generated 16-character password</p>
                    <p><strong>Step 7:</strong> Use this App Password, NOT your regular Gmail password</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
                <div class="info-box">
                    <h4>⚠️ Important Security Notes</h4>
                    <p>• <strong>Never use your regular Gmail password</strong> for SMTP</p>
                    <p>• App Passwords are 16 characters with no spaces</p>
                    <p>• 2-Step Verification must be enabled</p>
                    <p>• Each app password is unique and can be revoked</p>
                    <p>• Keep your app password secure and private</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
                <div class="info-box">
                    <h4>🔍 Troubleshooting Common Issues</h4>
                    <p><strong>Authentication Error:</strong> Double-check your app password</p>
                    <p><strong>Connection Error:</strong> Check your internet connection</p>
                    <p><strong>Recipient Refused:</strong> Verify the recipient email address</p>
                    <p><strong>2FA Required:</strong> Make sure 2-Step Verification is enabled</p>
                </div>
            """, unsafe_allow_html=True)
    
    # Maps Function Panel (Corrected)
    elif st.session_state.active_card == "maps":
        st.markdown("""
            <div class="function-panel">
                <div class="function-header">🗺️ Maps & Navigation</div>
            </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["📍 Find Location", "🛣️ Plan Route", "🌐 External Maps"])
        
        with tab1:
            st.markdown("### 📍 Search Location")
            
            col_m1, col_m2 = st.columns([2, 1])
            with col_m1:
                location_query = st.text_input("🏠 Enter Location", 
                                             placeholder="New York, NY or Times Square")
                
                if st.button("🔍 Search Location", key="search_location", use_container_width=True):
                    if location_query:
                        try:
                            with st.spinner("🔍 Searching location..."):
                                geolocator = Nominatim(user_agent="MultitaskHub_v2.0")
                                location = geolocator.geocode(location_query, timeout=10)
                                
                                if location:
                                    st.success(f"📍 Found: {location.address}")
                                    st.info(f"🌍 Coordinates: {location.latitude:.6f}, {location.longitude:.6f}")
                                    
                                    # Store in session state
                                    st.session_state.found_location = {
                                        'name': location.address,
                                        'lat': location.latitude,
                                        'lon': location.longitude
                                    }
                                else:
                                    st.error("❌ Location not found. Try a different search term.")
                        except Exception as e:
                            st.error(f"❌ Search error: {str(e)}")
                    else:
                        st.warning("⚠️ Please enter a location to search.")
            
            with col_m2:
                st.markdown("### 💡 Search Tips")
                st.info("• Try specific addresses\n• Use landmarks\n• Include city/state\n• Use proper spelling")
            
            # Display map if location found
            if hasattr(st.session_state, 'found_location') and st.session_state.found_location:
                try:
                    loc_data = st.session_state.found_location
                    m = folium.Map(location=[loc_data['lat'], loc_data['lon']], zoom_start=15)
                    folium.Marker([loc_data['lat'], loc_data['lon']], 
                                tooltip="📍 Found Location", 
                                popup=loc_data['name'],
                                icon=folium.Icon(color='red', icon='info-sign')).add_to(m)
                    st_folium(m, width=700, height=400)
                except Exception as e:
                    st.error(f"Map display error: {str(e)}")
        
        with tab2:
            st.markdown("### 🛣️ Route Planning")
            
            col_r1, col_r2 = st.columns([2, 1])
            with col_r1:
                start_location = st.text_input("🚀 Starting Point", 
                                             placeholder="Enter starting location")
                end_location = st.text_input("🎯 Destination", 
                                           placeholder="Enter destination")
                
                if st.button("🗺️ Plan Route", key="plan_route", use_container_width=True):
                    if start_location and end_location:
                        try:
                            with st.spinner("🗺️ Planning route..."):
                                geolocator = Nominatim(user_agent="MultitaskHub_v2.0")
                                start_loc = geolocator.geocode(start_location, timeout=10)
                                end_loc = geolocator.geocode(end_location, timeout=10)
                                
                                if start_loc and end_loc:
                                    # Calculate approximate distance using Haversine formula
                                    from math import radians, cos, sin, asin, sqrt
                                    
                                    def haversine(lon1, lat1, lon2, lat2):
                                        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
                                        dlon = lon2 - lon1
                                        dlat = lat2 - lat1
                                        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
                                        return 2 * asin(sqrt(a)) * 6371  # Earth radius in km
                                    
                                    distance = haversine(start_loc.longitude, start_loc.latitude, 
                                                       end_loc.longitude, end_loc.latitude)
                                    
                                    st.success(f"✅ Route planned successfully!")
                                    st.info(f"📏 Distance: {distance:.1f} km")
                                    
                                    # Store route data
                                    st.session_state.route_data = {
                                        'start': {'name': start_location, 'lat': start_loc.latitude, 'lon': start_loc.longitude},
                                        'end': {'name': end_location, 'lat': end_loc.latitude, 'lon': end_loc.longitude},
                                        'distance': distance
                                    }
                                else:
                                    st.error("❌ Could not find one or both locations.")
                        except Exception as e:
                            st.error(f"❌ Route planning error: {str(e)}")
                    else:
                        st.warning("⚠️ Please enter both starting point and destination.")
            
            with col_r2:
                st.markdown("### 🛣️ Route Info")
                st.info("• Plan routes between locations\n• Get distance estimates\n• Visual route display")
            
            # Display route map
            if hasattr(st.session_state, 'route_data') and st.session_state.route_data:
                try:
                    route = st.session_state.route_data
                    start = route['start']
                    end = route['end']
                    
                    # Calculate center point
                    center_lat = (start['lat'] + end['lat']) / 2
                    center_lon = (start['lon'] + end['lon']) / 2
                    
                    # Create map
                    m = folium.Map(location=[center_lat, center_lon], zoom_start=8)
                    
                    # Add markers
                    folium.Marker([start['lat'], start['lon']], 
                                tooltip="🚀 Start", popup=start['name'],
                                icon=folium.Icon(color='green', icon='play')).add_to(m)
                    folium.Marker([end['lat'], end['lon']], 
                                tooltip="🎯 End", popup=end['name'],
                                icon=folium.Icon(color='red', icon='stop')).add_to(m)
                    
                    # Add route line
                    folium.PolyLine(locations=[[start['lat'], start['lon']], [end['lat'], end['lon']]], 
                                  color="cyan", weight=4, opacity=0.7).add_to(m)
                    
                    st_folium(m, width=700, height=400)
                except Exception as e:
                    st.error(f"Route map error: {str(e)}")
        
        with tab3:
            st.markdown("### 🌐 Open in External Maps")
            
            external_location = st.text_input("🗺️ Location for External Maps", 
                                            placeholder="Enter location to open in external maps")
            
            col_ext1, col_ext2 = st.columns(2)
            with col_ext1:
                if st.button("📍 Open in Google Maps", key="open_google_maps", use_container_width=True):
                    if external_location:
                        try:
                            google_url = f"https://www.google.com/maps/search/{urllib.parse.quote(external_location)}"
                            st.markdown(f"""
                                <div class="success-message">
                                    ✅ Google Maps link created!
                                    <br><br>
                                    <a href="{google_url}" target="_blank" style="color: #00ffff; text-decoration: underline;">
                                        🔗 Open in Google Maps
                                    </a>
                                </div>
                            """, unsafe_allow_html=True)
                            webbrowser.open(google_url)
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                    else:
                        st.warning("⚠️ Please enter a location.")
            
            with col_ext2:
                if st.button("🗺️ Open in OpenStreetMap", key="open_osm", use_container_width=True):
                    if external_location:
                        try:
                            osm_url = f"https://www.openstreetmap.org/search?query={urllib.parse.quote(external_location)}"
                            st.markdown(f"""
                                <div class="success-message">
                                    ✅ OpenStreetMap link created!
                                    <br><br>
                                    <a href="{osm_url}" target="_blank" style="color: #00ffff; text-decoration: underline;">
                                        🔗 Open in OpenStreetMap
                                    </a>
                                </div>
                            """, unsafe_allow_html=True)
                            webbrowser.open(osm_url)
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                    else:
                        st.warning("⚠️ Please enter a location.")
    
    # System Monitor Panel (Corrected)
    elif st.session_state.active_card == "system":
        st.markdown("""
            <div class="function-panel">
                <div class="function-header">💻 System Monitor</div>
            </div>
        """, unsafe_allow_html=True)
        
        col_s1, col_s2 = st.columns(2)
        
        with col_s1:
            st.markdown("### 🧠 Memory (RAM) Information")
            if st.button("🔍 Check RAM Usage", key="check_ram"):
                try:
                    # Get memory information
                    memory = psutil.virtual_memory()
                    
                    st.markdown(f"""
                        <div class="info-box">
                            <h4>💾 RAM Statistics</h4>
                            <p><strong>Total RAM:</strong> {memory.total / (1024**3):.2f} GB</p>
                            <p><strong>Available:</strong> {memory.available / (1024**3):.2f} GB</p>
                            <p><strong>Used:</strong> {memory.used / (1024**3):.2f} GB</p>
                            <p><strong>Usage:</strong> {memory.percent}%</p>
                            <p><strong>Free:</strong> {memory.free / (1024**3):.2f} GB</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Create a simple progress bar
                    progress_bar = st.progress(0)
                    progress_bar.progress(memory.percent / 100)
                    
                except Exception as e:
                    st.error(f"❌ Error reading RAM info: {str(e)}")
        
        with col_s2:
            st.markdown("### 🖥️ CPU Information")
            if st.button("🔍 Check CPU Usage", key="check_cpu"):
                try:
                    # Get CPU information
                    cpu_percent = psutil.cpu_percent(interval=1)
                    cpu_count = psutil.cpu_count()
                    
                    try:
                        cpu_freq = psutil.cpu_freq()
                        current_freq = cpu_freq.current if cpu_freq else "N/A"
                        max_freq = cpu_freq.max if cpu_freq else "N/A"
                    except:
                        current_freq = "N/A"
                        max_freq = "N/A"
                    
                    st.markdown(f"""
                        <div class="info-box">
                            <h4>⚡ CPU Statistics</h4>
                            <p><strong>CPU Usage:</strong> {cpu_percent}%</p>
                            <p><strong>CPU Cores:</strong> {cpu_count}</p>
                            <p><strong>Current Freq:</strong> {current_freq if current_freq != "N/A" else "N/A"}</p>
                            <p><strong>Max Freq:</strong> {max_freq if max_freq != "N/A" else "N/A"}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Create a simple progress bar
                    progress_bar = st.progress(0)
                    progress_bar.progress(cpu_percent / 100)
                    
                except Exception as e:
                    st.error(f"❌ Error reading CPU info: {str(e)}")
        
        st.markdown("### 💽 Disk Information")
        if st.button("🔍 Check Disk Usage", key="check_disk"):
            try:
                # Get disk information for the root directory
                disk_usage = psutil.disk_usage('/' if os.name != 'nt' else 'C:\\')
                
                st.markdown(f"""
                    <div class="info-box">
                        <h4>💽 Disk Statistics</h4>
                        <p><strong>Total Disk:</strong> {disk_usage.total / (1024**3):.2f} GB</p>
                        <p><strong>Used:</strong> {disk_usage.used / (1024**3):.2f} GB</p>
                        <p><strong>Free:</strong> {disk_usage.free / (1024**3):.2f} GB</p>
                        <p><strong>Usage:</strong> {(disk_usage.used / disk_usage.total) * 100:.1f}%</p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Create a simple progress bar
                progress_bar = st.progress(0)
                progress_bar.progress((disk_usage.used / disk_usage.total))
                
            except Exception as e:
                st.error(f"❌ Error reading disk info: {str(e)}")
        
        # Additional system information
        st.markdown("### 🖥️ System Information")
        if st.button("📊 Get System Info", key="system_info"):
            try:
                import platform
                
                st.markdown(f"""
                    <div class="info-box">
                        <h4>🖥️ System Details</h4>
                        <p><strong>Operating System:</strong> {platform.system()} {platform.release()}</p>
                        <p><strong>Architecture:</strong> {platform.architecture()[0]}</p>
                        <p><strong>Processor:</strong> {platform.processor()}</p>
                        <p><strong>Python Version:</strong> {platform.python_version()}</p>
                        <p><strong>Machine:</strong> {platform.machine()}</p>
                    </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Error getting system info: {str(e)}")
    
    # SMS & Call Panel (Corrected)
    elif st.session_state.active_card == "sms":
        st.markdown("""
            <div class="function-panel">
                <div class="function-header">📞 SMS & Call Tools</div>
            </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["📱 Send SMS", "📞 Make Call", "🔧 Setup Instructions"])
        
        with tab1:
            st.markdown("### 📱 Send SMS")
            
            col_sms1, col_sms2 = st.columns([2, 1])
            with col_sms1:
                if twilio:
                    st.markdown("#### 🔐 Twilio Configuration")
                    account_sid = st.text_input("Account SID", type="password", help="Get from Twilio Console")
                    auth_token = st.text_input("Auth Token", type="password", help="Get from Twilio Console")
                    from_number = st.text_input("From Number", placeholder="+1234567890", help="Your Twilio phone number")
                    
                    st.markdown("#### 📱 SMS Details")
                    to_number = st.text_input("To Number", placeholder="+1987654321", help="Recipient's phone number")
                    sms_message = st.text_area("Message", placeholder="Your SMS message here...", height=100)
                    
                    if st.button("📤 Send SMS", key="send_sms"):
                        if all([account_sid, auth_token, from_number, to_number, sms_message]):
                            try:
                                client = Client(account_sid, auth_token)
                                message = client.messages.create(
                                    body=sms_message,
                                    from_=from_number,
                                    to=to_number
                                )
                                st.success(f"✅ SMS sent successfully! Message SID: {message.sid}")
                            except Exception as e:
                                st.error(f"❌ Error sending SMS: {str(e)}")
                        else:
                            st.warning("⚠️ Please fill in all fields.")
                else:
                    st.error("❌ Twilio library not installed. Install with: `pip install twilio`")
                    
                    st.markdown("#### 📧 Alternative: Email-to-SMS Gateway")
                    carrier_gateways = {
                        "Verizon": "vtext.com",
                        "AT&T": "txt.att.net",
                        "T-Mobile": "tmomail.net",
                        "Sprint": "messaging.sprintpcs.com",
                        "Cricket": "sms.cricketwireless.net"
                    }
                    
                    phone_sms = st.text_input("Phone Number", placeholder="1234567890 (numbers only)")
                    carrier = st.selectbox("Select Carrier", list(carrier_gateways.keys()))
                    sms_msg = st.text_area("SMS Message", placeholder="Your message...", height=80)
                    
                    if st.button("📤 Send via Email Gateway", key="send_email_sms"):
                        if phone_sms and sms_msg:
                            gateway_email = f"{phone_sms}@{carrier_gateways[carrier]}"
                            sms_url = f"mailto:{gateway_email}?body={urllib.parse.quote(sms_msg)}"
                            
                            st.markdown(f"""
                                <div class="success-message">
                                    ✅ SMS gateway email created!
                                    <br><br>
                                    <a href="{sms_url}" target="_blank" style="color: #00ffff; text-decoration: underline;">
                                        🔗 Send SMS via Email
                                    </a>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            try:
                                webbrowser.open(sms_url)
                            except:
                                pass
                        else:
                            st.warning("⚠️ Please enter phone number and message.")
            
            with col_sms2:
                st.markdown("### 💡 SMS Tips")
                st.info("• Twilio offers reliable SMS API\n• Email gateways are free but limited\n• Include country codes\n• Keep messages under 160 chars")
        
        with tab2:
            st.markdown("### 📞 Make Phone Call")
            
            col_call1, col_call2 = st.columns([2, 1])
            with col_call1:
                if twilio:
                    st.markdown("#### 🔐 Twilio Configuration")
                    call_account_sid = st.text_input("Account SID", type="password", key="call_sid")
                    call_auth_token = st.text_input("Auth Token", type="password", key="call_token")
                    call_from_number = st.text_input("From Number", placeholder="+1234567890", key="call_from")
                    
                    st.markdown("#### 📞 Call Details")
                    call_to_number = st.text_input("To Number", placeholder="+1987654321", key="call_to")
                    call_message = st.text_area("Voice Message", placeholder="Hello, this is a call from Python!", height=100, key="call_msg")
                    
                    if st.button("📞 Make Call", key="make_call"):
                        if all([call_account_sid, call_auth_token, call_from_number, call_to_number, call_message]):
                            try:
                                client = Client(call_account_sid, call_auth_token)
                                twiml_response = f'<Response><Say>{call_message}</Say></Response>'
                                
                                call = client.calls.create(
                                    twiml=twiml_response,
                                    to=call_to_number,
                                    from_=call_from_number
                                )
                                st.success(f"✅ Call initiated successfully! Call SID: {call.sid}")
                            except Exception as e:
                                st.error(f"❌ Error making call: {str(e)}")
                        else:
                            st.warning("⚠️ Please fill in all fields.")
                else:
                    st.error("❌ Twilio library not installed. Install with: `pip install twilio`")
                    
                    st.markdown("#### 📞 Alternative: Direct Dial")
                    direct_number = st.text_input("Phone Number", placeholder="+1234567890", key="direct_dial")
                    
                    if st.button("📞 Open Dialer", key="open_dialer"):
                        if direct_number:
                            dial_url = f"tel:{direct_number}"
                            st.markdown(f"""
                                <div class="success-message">
                                    ✅ Dialer link created!
                                    <br><br>
                                    <a href="{dial_url}" style="color: #00ffff; text-decoration: underline;">
                                        🔗 Call {direct_number}
                                    </a>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            try:
                                webbrowser.open(dial_url)
                            except:
                                pass
                        else:
                            st.warning("⚠️ Please enter a phone number.")
            
            with col_call2:
                st.markdown("### 💡 Call Tips")
                st.info("• Twilio supports programmable voice\n• Direct dialer works on mobile\n• Check local regulations\n• Test with your own number first")
        
        with tab3:
            st.markdown("### 🔧 Setup Instructions")
            
            st.markdown("""
                <div class="info-box">
                    <h4>📱 Twilio Setup (Recommended)</h4>
                    <p>1. Create account at <a href="https://www.twilio.com" target="_blank">twilio.com</a></p>
                    <p>2. Get a phone number from Twilio Console</p>
                    <p>3. Find your Account SID and Auth Token</p>
                    <p>4. Install Twilio: <code>pip install twilio</code></p>
                    <p>5. Add credits to your account for SMS/calls</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
                <div class="info-box">
                    <h4>📧 Email-to-SMS Gateway (Free)</h4>
                    <p>• Works through carrier email gateways</p>
                    <p>• No API keys required</p>
                    <p>• Limited formatting and reliability</p>
                    <p>• Good for basic notifications</p>
                </div>
            """, unsafe_allow_html=True)
    
    # Web Tools Panel (Corrected)
    elif st.session_state.active_card == "web":
        st.markdown("""
            <div class="function-panel">
                <div class="function-header">🌐 Web Tools & Scraping</div>
            </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔍 Google Search", "🕷️ Web Scraping"])
        
        with tab1:
            st.markdown("### 🔍 Google Search with Python")
            
            col_search1, col_search2 = st.columns([2, 1])
            with col_search1:
                search_query = st.text_input("🔍 Search Query", placeholder="Enter your search terms...")
                num_results = st.slider("Number of Results", min_value=1, max_value=20, value=5)
                
                if st.button("🚀 Search Google", key="google_search"):
                    if search_query:
                        if search:
                            try:
                                with st.spinner("🔍 Searching Google..."):
                                    results = list(search(search_query, num_results=num_results))
                                    
                                    st.success(f"✅ Found {len(results)} results for '{search_query}'")
                                    
                                    for i, url in enumerate(results, 1):
                                        st.markdown(f"""
                                            <div class="info-box">
                                                <h5>Result {i}</h5>
                                                <a href="{url}" target="_blank" style="color: #00ffff; text-decoration: underline;">
                                                    {url}
                                                </a>
                                            </div>
                                        """, unsafe_allow_html=True)
                                        
                            except Exception as e:
                                st.error(f"❌ Search error: {str(e)}")
                                st.info("💡 Try installing: `pip install googlesearch-python`")
                        else:
                            st.error("❌ Google search library not available. Install with: `pip install googlesearch-python`")
                            
                            # Alternative: Open Google search in browser
                            google_url = f"https://www.google.com/search?q={urllib.parse.quote(search_query)}"
                            st.markdown(f"""
                                <div class="success-message">
                                    ✅ Alternative: Open Google search in browser
                                    <br><br>
                                    <a href="{google_url}" target="_blank" style="color: #00ffff; text-decoration: underline;">
                                        🔗 Search on Google
                                    </a>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            try:
                                webbrowser.open(google_url)
                            except:
                                pass
                    else:
                        st.warning("⚠️ Please enter a search query.")
            
            with col_search2:
                st.markdown("### 💡 Search Tips")
                st.info("• Use specific keywords\n• Try different phrasings\n• Add quotes for exact phrases\n• Use site: for specific sites")
        
        with tab2:
            st.markdown("### 🕷️ Website Data Scraper")
            
            col_scrape1, col_scrape2 = st.columns([2, 1])
            with col_scrape1:
                scrape_url = st.text_input("🌐 Website URL", placeholder="https://example.com")
                scrape_type = st.selectbox("Scraping Type", ["Basic Info", "All Text", "All Links", "Images"])
                
                if st.button("🕷️ Scrape Website", key="scrape_web"):
                    if scrape_url:
                        try:
                            with st.spinner("🕷️ Scraping website..."):
                                headers = {
                                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                                }
                                response = requests.get(scrape_url, headers=headers, timeout=10)
                                response.raise_for_status()
                                
                                soup = BeautifulSoup(response.content, 'html.parser')
                                
                                if scrape_type == "Basic Info":
                                    title = soup.find('title')
                                    title_text = title.text.strip() if title else "No title found"
                                    
                                    meta_desc = soup.find('meta', attrs={'name': 'description'})
                                    desc_text = meta_desc.get('content', 'No description found') if meta_desc else "No description found"
                                    
                                    st.markdown(f"""
                                        <div class="info-box">
                                            <h4>📄 Website Information</h4>
                                            <p><strong>URL:</strong> {scrape_url}</p>
                                            <p><strong>Title:</strong> {title_text}</p>
                                            <p><strong>Description:</strong> {desc_text}</p>
                                            <p><strong>Status Code:</strong> {response.status_code}</p>
                                        </div>
                                    """, unsafe_allow_html=True)
                                
                                elif scrape_type == "All Text":
                                    text_content = soup.get_text()
                                    cleaned_text = ' '.join(text_content.split())[:2000]  # Limit to 2000 chars
                                    
                                    st.markdown("#### 📝 Website Text Content")
                                    st.text_area("Content Preview", cleaned_text, height=300, disabled=True)
                                
                                elif scrape_type == "All Links":
                                    links = soup.find_all('a', href=True)
                                    
                                    st.markdown(f"#### 🔗 Found {len(links)} Links")
                                    for i, link in enumerate(links[:20], 1):  # Show first 20 links
                                        href = link['href']
                                        text = link.text.strip() or "No text"
                                        
                                        if href.startswith('http'):
                                            full_url = href
                                        elif href.startswith('/'):
                                            base_url = '/'.join(scrape_url.split('/')[:3])
                                            full_url = f"{base_url}{href}"
                                        else:
                                            base_url = scrape_url.rstrip('/')
                                            full_url = f"{base_url}/{href}"
                                        
                                        st.markdown(f"{i}. [{text[:50]}...]({full_url})")
                                
                                elif scrape_type == "Images":
                                    images = soup.find_all('img', src=True)
                                    
                                    st.markdown(f"#### 🖼️ Found {len(images)} Images")
                                    for i, img in enumerate(images[:10], 1):  # Show first 10 images
                                        src = img['src']
                                        alt = img.get('alt', 'No alt text')
                                        
                                        if src.startswith('http'):
                                            img_url = src
                                        elif src.startswith('/'):
                                            base_url = '/'.join(scrape_url.split('/')[:3])
                                            img_url = f"{base_url}{src}"
                                        else:
                                            base_url = scrape_url.rstrip('/')
                                            img_url = f"{base_url}/{src}"
                                        
                                        st.markdown(f"{i}. Alt: {alt}")
                                        st.markdown(f"   URL: {img_url}")
                                
                        except requests.exceptions.RequestException as e:
                            st.error(f"❌ Network error: {str(e)}")
                        except Exception as e:
                            st.error(f"❌ Scraping error: {str(e)}")
                            st.info("💡 Make sure the URL is accessible and includes http:// or https://")
                    else:
                        st.warning("⚠️ Please enter a website URL.")
            
            with col_scrape2:
                st.markdown("### ⚠️ Scraping Notes")
                st.info("• Respect robots.txt\n• Don't overload servers\n• Some sites block scrapers\n• Check terms of service")
    
    # Programming Tools Panel (Corrected)
    elif st.session_state.active_card == "programming":
        st.markdown("""
            <div class="function-panel">
                <div class="function-header">🐍 Programming Concepts</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📚 Technical Difference: Tuple vs List")
        
        col_prog1, col_prog2 = st.columns(2)
        
        with col_prog1:
            st.markdown("""
                <div class="info-box">
                    <h4>📋 Lists</h4>
                    <p><strong>Mutability:</strong> Mutable (can be changed)</p>
                    <p><strong>Syntax:</strong> [1, 2, 3, 4]</p>
                    <p><strong>Performance:</strong> Slower for large datasets</p>
                    <p><strong>Memory:</strong> More memory usage</p>
                    <p><strong>Methods:</strong> append(), remove(), pop(), etc.</p>
                    <p><strong>Use Case:</strong> When you need to modify data</p>
                    <p><strong>Hashable:</strong> No (can't be dict keys)</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col_prog2:
            st.markdown("""
                <div class="info-box">
                    <h4>📦 Tuples</h4>
                    <p><strong>Mutability:</strong> Immutable (cannot be changed)</p>
                    <p><strong>Syntax:</strong> (1, 2, 3, 4)</p>
                    <p><strong>Performance:</strong> Faster for large datasets</p>
                    <p><strong>Memory:</strong> Less memory usage</p>
                    <p><strong>Methods:</strong> count(), index() only</p>
                    <p><strong>Use Case:</strong> For fixed data, coordinates</p>
                    <p><strong>Hashable:</strong> Yes (can be dict keys)</p>
                </div>
            """, unsafe_allow_html=True)
        
        # Interactive demonstration
        st.markdown("### 🧪 Interactive Demonstration")
        
        demo_type = st.selectbox("Choose Demo", ["Performance Test", "Memory Usage", "Practical Examples"])
        
        if demo_type == "Performance Test":
            if st.button("⚡ Run Performance Test", key="perf_test"):
                with st.spinner("Running performance tests..."):
                    import time
                    
                    # Test list creation
                    start_time = time.time()
                    test_list = [i for i in range(100000)]
                    list_time = time.time() - start_time
                    
                    # Test tuple creation
                    start_time = time.time()
                    test_tuple = tuple(i for i in range(100000))
                    tuple_time = time.time() - start_time
                    
                    # Test access speed
                    start_time = time.time()
                    for _ in range(1000):
                        _ = test_list[50000]
                    list_access_time = time.time() - start_time
                    
                    start_time = time.time()
                    for _ in range(1000):
                        _ = test_tuple[50000]
                    tuple_access_time = time.time() - start_time
                    
                    st.markdown(f"""
                        <div class="code-box">
                            Performance Test Results (100,000 elements):
                            
                            Creation Time:
                            • List:  {list_time:.6f} seconds
                            • Tuple: {tuple_time:.6f} seconds
                            
                            Access Time (1000 iterations):
                            • List:  {list_access_time:.6f} seconds  
                            • Tuple: {tuple_access_time:.6f} seconds
                            
                            Winner: {'Tuple' if tuple_time < list_time else 'List'} for creation
                            Winner: {'Tuple' if tuple_access_time < list_access_time else 'List'} for access
                        </div>
                    """, unsafe_allow_html=True)
        
        elif demo_type == "Memory Usage":
            if st.button("📊 Check Memory Usage", key="memory_test"):
                import sys
                
                # Create test data
                test_list = [1, 2, 3, 4, 5] * 1000
                test_tuple = tuple(test_list)
                
                list_size = sys.getsizeof(test_list)
                tuple_size = sys.getsizeof(test_tuple)
                
                st.markdown(f"""
                    <div class="code-box">
                        Memory Usage Comparison (5000 elements):
                        
                        • List size:  {list_size} bytes
                        • Tuple size: {tuple_size} bytes
                        
                        Difference: {list_size - tuple_size} bytes
                        Tuple is {((list_size - tuple_size) / list_size * 100):.1f}% smaller
                    </div>
                """, unsafe_allow_html=True)
        
        elif demo_type == "Practical Examples":
            st.markdown("""
                <div class="code-box">
                    # List Example - Shopping Cart (mutable data)
                    shopping_cart = ['apple', 'banana']
                    shopping_cart.append('orange')    # ✅ Works
                    shopping_cart.remove('banana')    # ✅ Works
                    print(shopping_cart)  # ['apple', 'orange']
                    
                    # Tuple Example - Coordinates (immutable data)
                    coordinates = (40.7128, -74.0060)  # NYC coordinates
                    # coordinates.append(100)          # ❌ Error!
                    # coordinates[0] = 50              # ❌ Error!
                    
                    # Tuple as Dictionary Key
                    locations = {
                        (40.7128, -74.0060): "New York",
                        (34.0522, -118.2437): "Los Angeles"
                    }
                    
                    # List cannot be used as dict key
                    # locations[[40.7128, -74.0060]] = "NYC"  # ❌ Error!
                </div>
            """, unsafe_allow_html=True)
    
    # Image Tools Panel (Corrected)
    elif st.session_state.active_card == "image":
        st.markdown("""
            <div class="function-panel">
                <div class="function-header">🖼️ Image Creation & Editing Tools</div>
            </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🎨 Create Digital Image", "🔧 Image Effects"])
        
        with tab1:
            st.markdown("### 🎨 Create Your Own Digital Image")
            
            col_img1, col_img2 = st.columns([2, 1])
            with col_img1:
                # Image creation parameters
                img_width = st.slider("Image Width", min_value=100, max_value=800, value=400)
                img_height = st.slider("Image Height", min_value=100, max_value=600, value=300)
                bg_color = st.color_picker("Background Color", value="#000080")
                
                # Text parameters
                text_content = st.text_input("Text to Add", value="Hello World!")
                text_color = st.color_picker("Text Color", value="#00FFFF")
                text_size = st.slider("Text Size", min_value=10, max_value=100, value=30)
                
                # Shape parameters
                add_shapes = st.checkbox("Add Shapes")
                if add_shapes:
                    shape_type = st.selectbox("Shape Type", ["Circle", "Rectangle", "Line"])
                    shape_color = st.color_picker("Shape Color", value="#FF0000")
                
                if st.button("🎨 Generate Image", key="create_image"):
                    try:
                        # Create image with user-selected background color
                        img = Image.new('RGB', (img_width, img_height), color=bg_color)
                        draw = ImageDraw.Draw(img)

                        # Add text if not empty
                        if text_content.strip():
                            try:
                                # Try to load a system font
                                font = ImageFont.truetype("arial.ttf", text_size)
                            except (OSError, IOError):
                                try:
                                    font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", text_size)
                                except (OSError, IOError):
                                    font = ImageFont.load_default()
                            
                            # Get text size for centering
                            try:
                                bbox = draw.textbbox((0, 0), text_content, font=font)
                                text_width = bbox[2] - bbox[0]
                                text_height = bbox[3] - bbox[1]
                            except AttributeError:
                                # Fallback for older PIL versions
                                text_width, text_height = draw.textsize(text_content, font=font)
                            
                            x = (img_width - text_width) // 2
                            y = (img_height - text_height) // 2
                            draw.text((x, y), text_content, fill=text_color, font=font)

                        # Add shapes
                        if add_shapes:
                            if shape_type == "Circle":
                                center_x, center_y = img_width // 2, img_height // 4
                                radius = min(50, img_width // 8, img_height // 8)
                                draw.ellipse(
                                    [center_x - radius, center_y - radius, center_x + radius, center_y + radius],
                                    fill=shape_color
                                )
                            elif shape_type == "Rectangle":
                                rect_x0 = img_width // 4
                                rect_y0 = img_height // 6
                                rect_x1 = 3 * img_width // 4
                                rect_y1 = img_height // 3
                                draw.rectangle([rect_x0, rect_y0, rect_x1, rect_y1], fill=shape_color, outline=shape_color)
                            elif shape_type == "Line":
                                draw.line([(50, img_height // 2), (img_width - 50, img_height // 2)], fill=shape_color, width=5)

                        # Display image in Streamlit
                        st.image(img, caption="Generated Image", use_column_width=True)
                        
                        # Provide download option
                        buf = io.BytesIO()
                        img.save(buf, format='PNG')
                        buf.seek(0)
                        
                        st.download_button(
                            label="💾 Download Image",
                            data=buf,
                            file_name="generated_image.png",
                            mime="image/png",
                            use_container_width=True
                        )

                    except Exception as e:
                        st.error(f"❌ Error generating image: {str(e)}")
            
            with col_img2:
                st.markdown("### 🎨 Image Tips")
                st.info("• Try different color combinations\n• Adjust text size for readability\n• Shapes add visual interest\n• Download your creations")
        
        with tab2:
            st.markdown("### 🔧 Image Effects & Filters")
            
            uploaded_file = st.file_uploader("📁 Upload an Image", type=['png', 'jpg', 'jpeg'])
            
            if uploaded_file is not None:
                try:
                    # Load the uploaded image
                    image = Image.open(uploaded_file)
                    st.image(image, caption="Original Image", use_column_width=True)
                    
                    # Image effects options
                    effect_type = st.selectbox("Choose Effect", ["Grayscale", "Blur", "Brightness", "Contrast"])
                    
                    if effect_type == "Grayscale":
                        if st.button("🎨 Apply Grayscale", key="apply_grayscale"):
                            grayscale_img = image.convert('L')
                            st.image(grayscale_img, caption="Grayscale Image", use_column_width=True)
                            
                            # Download option
                            buf = io.BytesIO()
                            grayscale_img.save(buf, format='PNG')
                            buf.seek(0)
                            st.download_button("💾 Download Grayscale", buf, "grayscale_image.png", "image/png")
                    
                    elif effect_type == "Brightness":
                        brightness = st.slider("Brightness Level", 0.1, 3.0, 1.0, 0.1)
                        if st.button("🎨 Apply Brightness", key="apply_brightness"):
                            from PIL import ImageEnhance
                            enhancer = ImageEnhance.Brightness(image)
                            bright_img = enhancer.enhance(brightness)
                            st.image(bright_img, caption=f"Brightness: {brightness}", use_column_width=True)
                            
                            buf = io.BytesIO()
                            bright_img.save(buf, format='PNG')
                            buf.seek(0)
                            st.download_button("💾 Download Bright Image", buf, "bright_image.png", "image/png")
                    
                    elif effect_type == "Contrast":
                        contrast = st.slider("Contrast Level", 0.1, 3.0, 1.0, 0.1)
                        if st.button("🎨 Apply Contrast", key="apply_contrast"):
                            from PIL import ImageEnhance
                            enhancer = ImageEnhance.Contrast(image)
                            contrast_img = enhancer.enhance(contrast)
                            st.image(contrast_img, caption=f"Contrast: {contrast}", use_column_width=True)
                            
                            buf = io.BytesIO()
                            contrast_img.save(buf, format='PNG')
                            buf.seek(0)
                            st.download_button("💾 Download Contrast Image", buf, "contrast_image.png", "image/png")
                    
                    elif effect_type == "Blur":
                        blur_radius = st.slider("Blur Radius", 0, 10, 2)
                        if st.button("🎨 Apply Blur", key="apply_blur"):
                            from PIL import ImageFilter
                            blurred_img = image.filter(ImageFilter.GaussianBlur(radius=blur_radius))
                            st.image(blurred_img, caption=f"Blur Radius: {blur_radius}", use_column_width=True)
                            
                            buf = io.BytesIO()
                            blurred_img.save(buf, format='PNG')
                            buf.seek(0)
                            st.download_button("💾 Download Blurred Image", buf, "blurred_image.png", "image/png")
                
                except Exception as e:
                    st.error(f"❌ Error processing image: {str(e)}")
            else:
                st.info("📁 Upload an image to apply effects and filters!")
    
    # AI Tools Panel (Corrected)
    elif st.session_state.active_card == "ai":
        st.markdown("""
            <div class="function-panel">
                <div class="function-header">🤖 AI Models Comparison</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🤖 Popular AI Models Comparison")
        
        # AI Models Data
        ai_models = {
            "GPT-4": {
                "company": "OpenAI",
                "type": "Language Model",
                "parameters": "~1.76T",
                "strengths": "Reasoning, coding, creative writing",
                "use_cases": "Chatbots, content creation, programming",
                "cost": "High",
                "availability": "API, ChatGPT Plus"
            },
            "Claude": {
                "company": "Anthropic",
                "type": "Language Model", 
                "parameters": "Unknown",
                "strengths": "Safety, helpful responses, analysis",
                "use_cases": "Research, writing, analysis",
                "cost": "Medium",
                "availability": "API, Web interface"
            },
            "Gemini": {
                "company": "Google",
                "type": "Multimodal",
                "parameters": "Unknown",
                "strengths": "Multimodal, integration with Google services",
                "use_cases": "Search, productivity, multimodal tasks",
                "cost": "Medium",
                "availability": "API, Bard"
            },
            "LLaMA 2": {
                "company": "Meta",
                "type": "Language Model",
                "parameters": "7B-70B",
                "strengths": "Open source, customizable",
                "use_cases": "Research, custom applications",
                "cost": "Free",
                "availability": "Open source"
            }
        }
        
        # Create comparison table
        col_ai1, col_ai2 = st.columns([3, 1])
        
        with col_ai1:
            selected_models = st.multiselect(
                "Select AI Models to Compare",
                list(ai_models.keys()),
                default=["GPT-4", "Claude"]
            )
            
            if selected_models:
                comparison_data = []
                for model in selected_models:
                    data = ai_models[model]
                    comparison_data.append({
                        "Model": model,
                        "Company": data["company"],
                        "Type": data["type"],
                        "Parameters": data["parameters"],
                        "Strengths": data["strengths"],
                        "Cost": data["cost"],
                        "Availability": data["availability"]
                    })
                
                # Display comparison
                for model_data in comparison_data:
                    st.markdown(f"""
                        <div class="info-box">
                            <h4>🤖 {model_data['Model']}</h4>
                            <p><strong>Company:</strong> {model_data['Company']}</p>
                            <p><strong>Type:</strong> {model_data['Type']}</p>
                            <p><strong>Parameters:</strong> {model_data['Parameters']}</p>
                            <p><strong>Strengths:</strong> {model_data['Strengths']}</p>
                            <p><strong>Cost:</strong> {model_data['Cost']}</p>
                            <p><strong>Availability:</strong> {model_data['Availability']}</p>
                        </div>
                    """, unsafe_allow_html=True)
        
        with col_ai2:
            st.markdown("### 🔍 AI Categories")
            st.info("• Language Models\n• Image Generation\n• Code Assistants\n• Multimodal AI\n• Specialized AI")
            
            st.markdown("### 💡 Selection Tips")
            st.info("• Consider your use case\n• Check pricing models\n• Test API availability\n• Review safety features")
        
        # Performance metrics visualization
        st.markdown("### 📊 Performance Comparison")
        
        if st.button("📈 Show Performance Chart", key="show_performance"):
            # Sample performance data (you can replace with real benchmarks)
            performance_data = {
                "Model": ["GPT-4", "Claude", "Gemini", "LLaMA 2"],
                "Reasoning": [95, 90, 85, 75],
                "Coding": [90, 85, 80, 70],
                "Creative Writing": [92, 88, 82, 78],
                "Safety": [85, 95, 80, 70]
            }
            
            import pandas as pd
            df = pd.DataFrame(performance_data)
            
            st.bar_chart(df.set_index('Model'))
            
            st.info("📊 Performance scores are illustrative and may vary based on specific tasks and evaluation methods.")

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; padding: 2rem 0; color: #666;">
        <p>🚀 Advanced Multitask Hub v2.0 | Built with Streamlit & Python</p>
        <p>💡 Professional toolkit for productivity and automation</p>
    </div>
""", unsafe_allow_html=True)