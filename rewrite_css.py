import re

def rewrite():
    path = '../styles.css'
    with open(path, 'r', encoding='utf-8') as f:
        css = f.read()

    # Change gold themes to green themes
    css = css.replace('--gold-900', '--green-900')
    css = css.replace('--gold-800', '--green-800')
    css = css.replace('--gold-700', '--green-700')
    css = css.replace('--gold-600', '--green-600')
    css = css.replace('--gold-500', '--green-500')
    css = css.replace('--gold-400', '--green-400')
    css = css.replace('--gold-300', '--green-300')
    css = css.replace('--gold-200', '--green-200')
    css = css.replace('--gold-100', '--green-100')

    # deep-gold class -> deep-green
    css = css.replace('deep-gold', 'deep-green')
    css = css.replace('black-gold', 'black-green')

    # Replace specific gold hue variables (around 43-45 hue) with green (around 140-150 hue)
    # The user's prompt says "maintain the premium glassmorphism and modern UI feel"
    # We will just change hue in hsl/hsla
    # Actually, a regex replacement for HSL colors to shift hue:
    
    def shift_hue(match):
        h, s, l = match.group(1), match.group(2), match.group(3)
        h_val = int(h)
        # Shift gold (40-50) to green (145)
        if 35 <= h_val <= 60:
            h_val = 145
        return f"hsl({h_val} {s} {l})"
        
    css = re.sub(r'hsl\(\s*(\d+)\s+(\d+%)\s+(\d+%)\s*\)', shift_hue, css)
    
    def shift_hsla(match):
        h, s, l, a = match.group(1), match.group(2), match.group(3), match.group(4)
        h_val = int(h)
        if 35 <= h_val <= 60:
            h_val = 145
        return f"hsl({h_val} {s} {l} / {a})"
        
    css = re.sub(r'hsl\(\s*(\d+)\s+(\d+%)\s+(\d+%)\s*/\s*([^)]+)\)', shift_hsla, css)
    
    # Check for rgb colors
    # --primary: #f6cf63; -> #4caf50
    css = css.replace('#f6cf63', '#4caf50')
    css = css.replace('#d9a928', '#8bc34a')
    css = css.replace('#b8860b', '#388e3c')
    css = css.replace('#7f6a2f', '#1b5e20')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(css)

if __name__ == '__main__':
    rewrite()
    print("Done")
