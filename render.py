#!/usr/bin/env python3
"""
render.py - Generates the newspaper front page draft (entry.png) for 24 November 2026.
Masthead, date line, and LEAD story with a stylised map illustration.
"""

import os
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1024
HEIGHT = 1024

PAPER_BG = (251, 251, 250)
BLACK_INK = (20, 20, 20)
RED_ACCENT = (180, 30, 30)
MUTED_GREY = (70, 70, 70)
LIGHT_RULE = (180, 180, 180)
LIGHT_RED_TINT = (245, 220, 220)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

def get_fonts():
    try:
        serif_bold = ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf"), 42)
        serif_bold_lead = ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf"), 20)
        serif_body = ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSerif.ttf"), 12)
        sans_bold = ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"), 13)
        sans_bold_kicker = ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"), 11)
    except IOError:
        serif_bold = ImageFont.load_default()
        serif_bold_lead = ImageFont.load_default()
        serif_body = ImageFont.load_default()
        sans_bold = ImageFont.load_default()
        sans_bold_kicker = ImageFont.load_default()
    return serif_bold, serif_bold_lead, serif_body, sans_bold, sans_bold_kicker

def wrap_text(text, font, max_width):
    words = text.split()
    if not words:
        return []
    lines = []
    current_line = []
    for word in words:
        test_line = " ".join(current_line + [word])
        bbox = font.getbbox(test_line)
        width = bbox[2] - bbox[0]
        if width <= max_width or not current_line:
            current_line.append(word)
        else:
            lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))
    return lines

def render():
    image = Image.new("RGB", (WIDTH, HEIGHT), PAPER_BG)
    draw = ImageDraw.Draw(image)
    
    serif_bold, serif_bold_lead, serif_body, sans_bold, sans_bold_kicker = get_fonts()
    
    margin = 32
    
    # Masthead
    draw.rectangle([margin, 24, WIDTH - margin, 26], fill=BLACK_INK)
    
    title_text = "THE DAILY CHRONICLE"
    bbox = serif_bold.getbbox(title_text)
    title_width = bbox[2] - bbox[0]
    title_x = (WIDTH - title_width) // 2
    draw.text((title_x, 30), title_text, font=serif_bold, fill=BLACK_INK)
    
    date_text = "TUESDAY, 24 NOVEMBER 2026 · WORLD NEWS EDITION"
    bbox_date = sans_bold.getbbox(date_text)
    date_width = bbox_date[2] - bbox_date[0]
    date_x = (WIDTH - date_width) // 2
    draw.text((date_x, 78), date_text, font=sans_bold, fill=RED_ACCENT)
    
    draw.rectangle([margin, 98, WIDTH - margin, 99], fill=BLACK_INK)
    
    # Lead story block
    lead_y = 112
    max_text_width = 610
    
    kicker_text = "RUSSIA — ESTONIA STANDOFF"
    draw.text((margin, lead_y), kicker_text, font=sans_bold_kicker, fill=RED_ACCENT)
    
    headline_text = "RUSSIA THREATENS ESTONIA WITH 'OPEN WAR'"
    headline_lines = wrap_text(headline_text, serif_bold_lead, max_text_width)
    
    headline_y = lead_y + 18
    for line in headline_lines:
        draw.text((margin, headline_y), line, font=serif_bold_lead, fill=BLACK_INK)
        headline_y += 26
        
    body_text = "Moscow accuses Tallinn of 'hostile actions', citing Estonia's move to close its land border crossings with Russia and claiming Estonia is allowing Ukraine to launch attacks from its soil. Russia summoned Estonia's diplomat to deliver a formal protest."
    body_lines = wrap_text(body_text, serif_body, max_text_width)
    
    body_y = headline_y + 10
    for line in body_lines:
        draw.text((margin, body_y), line, font=serif_body, fill=BLACK_INK)
        body_y += 18
        
    # Right illustration (x from 680 to 992)
    map_x1 = 680
    map_y1 = 112
    map_x2 = 992
    map_y2 = 270  # Shrank illustration so bottom edge ends at y=270 at the latest
    
    draw.rectangle([map_x1, map_y1, map_x2, map_y2], outline=LIGHT_RULE, width=1)
    
    land1_box = [map_x1 + 20, map_y1 + 16, map_x1 + 140, map_y2 - 16]
    draw.rectangle(land1_box, fill=LIGHT_RED_TINT, outline=BLACK_INK, width=2)
    
    land2_box = [map_x1 + 160, map_y1 + 16, map_x2 - 20, map_y2 - 16]
    draw.rectangle(land2_box, fill=(240, 240, 238), outline=BLACK_INK, width=2)
    
    dash_x = map_x1 + 150
    dash_y_start = map_y1 + 24
    dash_y_end = map_y2 - 24
    for dy in range(int(dash_y_start), int(dash_y_end), 10):
        draw.line([(dash_x, dy), (dash_x, min(dy + 5, dash_y_end))], fill=RED_ACCENT, width=3)
        
    tri_x = map_x1 + 80
    tri_y = map_y1 + 45
    triangle_points = [(tri_x, tri_y), (tri_x - 16, tri_y + 28), (tri_x + 16, tri_y + 28)]
    draw.polygon(triangle_points, fill=RED_ACCENT, outline=BLACK_INK)
    draw.rectangle([tri_x - 2, tri_y + 8, tri_x + 2, tri_y + 16], fill=PAPER_BG)
    draw.ellipse([tri_x - 2, tri_y + 20, tri_x + 2, tri_y + 24], fill=PAPER_BG)
    
    for gx in range(map_x1 + 40, map_x2 - 20, 50):
        draw.line([(gx, map_y1 + 8), (gx, map_y1 + 12)], fill=MUTED_GREY, width=1)
        draw.line([(gx, map_y2 - 12), (gx, map_y2 - 8)], fill=MUTED_GREY, width=1)

    # 1px black rule across content width at y=300
    draw.rectangle([margin, 300, WIDTH - margin, 301], fill=BLACK_INK)

    # Five stories in two columns below y=300
    # Left column: x=32, width ~460 (col_width = 460, right edge = 32 + 460 = 492)
    # Right column: x=532, width ~460 (col_width = 460, right edge = 532 + 460 = 992)
    
    left_x = 32
    left_width = 460
    right_x = 532
    right_width = 460
    
    stories_left = [
        {
            "kicker": "TRUMP WARNS IRAN",
            "headline": "TRUMP WARNS IRAN OF 'VERY TRAUMATIC' OUTCOME",
            "body": "President Trump warns Iran of a 'very traumatic' outcome if a nuclear deal fails, as the US imposes new Iran-related sanctions and weighs sending a second aircraft carrier to the Middle East. Iran vows 'every means' against the US blockade in the Strait of Hormuz."
        },
        {
            "kicker": "UKRAINE PEACE PUSH",
            "headline": "US OPEN TO NATO-STYLE GUARANTEES FOR KYIV",
            "body": "US envoy Jared Kushner says President Trump is open to NATO-style 'Article 5-like' security guarantees for Ukraine. President Zelenskyy confirms Ukraine sank a Russian warship off the Libyan coast near Benghazi."
        },
        {
            "kicker": "MANCHESTER ARENA EVACUATED",
            "headline": "12,000 FLEE CONCERT AFTER MYSTERY SUBSTANCE RELEASED",
            "body": "More than 12,000 fans were evacuated from a Don Toliver concert at Manchester's Co-op Live arena after an unknown substance was released in the crowd; 89 people showed symptoms, one taken to hospital. The rapper's London show is postponed."
        }
    ]
    
    stories_right = [
        {
            "kicker": "EU'S NEW RUSSIA SANCTIONS",
            "headline": "EU TARGETS BANKS, CRYPTO AND SPORT IN NEW PACKAGE",
            "body": "The European Union proposes sweeping new sanctions on Russia targeting banks, crypto and sports events."
        },
        {
            "kicker": "ARMENIA'S PEACE GAMBLE",
            "headline": "PASHINYAN DROPS KARABAKH CLAIM IN DRAFT CHARTER",
            "body": "Armenian PM Nikol Pashinyan unveils a draft constitution dropping the claim to the Karabakh region, saying it is the only way to reach a peace deal with Azerbaijan."
        }
    ]

    # Render left column starting at y = 315, spaced out to fill the page down to ~900
    curr_y_left = 315
    for s in stories_left:
        draw.text((left_x, curr_y_left), s["kicker"], font=sans_bold_kicker, fill=RED_ACCENT)
        curr_y_left += 18
        
        h_lines = wrap_text(s["headline"], sans_bold, left_width)
        for hl in h_lines:
            draw.text((left_x, curr_y_left), hl, font=sans_bold, fill=BLACK_INK)
            curr_y_left += 22
            
        curr_y_left += 8
        
        b_lines = wrap_text(s["body"], serif_body, left_width)
        for bl in b_lines:
            draw.text((left_x, curr_y_left), bl, font=serif_body, fill=BLACK_INK)
            curr_y_left += 22
            
        curr_y_left += 50

    # Render right column starting at y = 315, spaced out gracefully
    curr_y_right = 315
    for s in stories_right:
        draw.text((right_x, curr_y_right), s["kicker"], font=sans_bold_kicker, fill=RED_ACCENT)
        curr_y_right += 18
        
        h_lines = wrap_text(s["headline"], sans_bold, right_width)
        for hl in h_lines:
            draw.text((right_x, curr_y_right), hl, font=sans_bold, fill=BLACK_INK)
            curr_y_right += 22
            
        curr_y_right += 8
        
        b_lines = wrap_text(s["body"], serif_body, right_width)
        for bl in b_lines:
            draw.text((right_x, curr_y_right), bl, font=serif_body, fill=BLACK_INK)
            curr_y_right += 22
            
        curr_y_right += 110

    # Add a footer at the bottom: a 1px rule at y=985 and centred small grey text at y=992
    draw.rectangle([margin, 985, WIDTH - margin, 986], fill=LIGHT_RULE)
    footer_text = "THE DAILY CHRONICLE — TUESDAY, 24 NOVEMBER 2026 — WORLD NEWS IN ONE IMAGE"
    footer_font = ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"), 9)
    bbox_f = footer_font.getbbox(footer_text)
    f_width = bbox_f[2] - bbox_f[0]
    f_x = (WIDTH - f_width) // 2
    draw.text((f_x, 990), footer_text, font=footer_font, fill=MUTED_GREY)
        
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    image.save(output_path, "PNG")
    print(f"Saved {output_path}")

if __name__ == "__main__":
    render()
