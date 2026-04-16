import json

def create_champion_website(json_file, local_gif_name):
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Fehler: {json_file} nicht gefunden.")
        return

    members = data[:25]
    monate_namen = [
        "Januar", "Februar", "März", "April", "Mai", "Juni",
        "Juli", "August", "September", "Oktober", "November", "Dezember"
    ]

    # --- CHAMPION LOGIK ---
    max_sun_netto = -1
    champion_name = ""

    for m in members:
        s_netto = sum(m.get("netto_monate", []))
        if s_netto > max_sun_netto:
            max_sun_netto = s_netto
            champion_name = m.get("name", "")

    html_content = f"""
    <!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8">
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400..900;1,6..96,400..900&display=swap" rel="stylesheet">
        <title>Team Cashboard Center XX/VI</title>
        <style>
            body {{
                background-image: url('{local_gif_name}');
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
                margin: 0;
                overflow: hidden;
                font-family: 'Bodoni Moda', serif;
            }}

            .bg-overlay {{ 
                background-color: rgba(0, 0, 0, 0.65); 
                height: 100vh; 
                width: 100vw; 
                display: flex;
                flex-direction: column;
                justify-content: center; 
                align-items: center;     
            }}

            .compact-cell {{ width: calc(100vw / 27); min-width: 0; }}

            /* Switch-Farben Logik */
            /* Netto: Emerald Green */
            .mode-netto .val-brutto {{ display: none; }}
            .text-netto {{ color: #10b981; text-shadow: 0 0 15px rgba(16, 185, 129, 0.4); }} 

            /* Brutto: Gold / Amber */
            .mode-brutto .val-netto {{ display: none; }}
            .text-brutto {{ color: #fbbf24; text-shadow: 0 0 15px rgba(251, 191, 36, 0.4); }}

            .val-netto, .val-brutto {{
                animation: fadeIn 0.5s ease-in-out;
            }}

            @keyframes fadeIn {{
                from {{ opacity: 0; transform: scale(0.95); }}
                to {{ opacity: 1; transform: scale(1); }}
            }}

            .crown {{
                position: absolute;
                top: -2px; 
                left: 40%;
                transform: translateX(-50%) rotate(-15deg);
                font-size: 18px;
                color: #f59e0b;
                text-shadow: 0 0 12px rgba(245, 158, 11, 0.9), 0 0 3px rgba(0,0,0,1);
                z-index: 50;
                pointer-events: none;
            }}

            .font-numbers {{
                font-family: 'Bodoni Moda', serif;
                font-variant-numeric: tabular-nums;
            }}
        </style>
    </head>
    <body class="text-white mode-netto" id="main-body">
        <div class="bg-overlay p-4">

            <header class="mb-6">
                <h1 class="text-5xl font-black uppercase tracking-[0.3em] text-white/90 drop-shadow-[0_0_30px_rgba(0,0,0,0.8)] text-center italic">
                    Cashboard Center <span class="text-emerald-500">XX</span>/<span class="text-amber-500">VI</span>
                </h1>
            </header>

            <div class="w-[98vw] bg-black/30 backdrop-blur-md rounded-xl border border-white/10 shadow-2xl overflow-hidden mb-8">
                <table class="w-full table-fixed border-collapse">
                    <thead>
                        <tr class="bg-white/5">
                            <th class="w-24 pt-5 pb-2 border-r border-white/10 uppercase font-bold text-gray-400 text-[11px] tracking-widest">Monat</th>
                            {" ".join([f'''
                            <th class="pt-5 pb-1 border-r border-white/10 text-center compact-cell relative">
                                {'<div class="crown">👑</div>' if m['name'] == champion_name else ''}
                                <img src="https://ui-avatars.com/api/?name={m['name'].replace(" ", "+")}&background=random&color=fff&size=40" 
                                     class="w-7 h-7 rounded-full mx-auto mb-1 border border-white/20 shadow-sm relative z-0">
                                <div class="text-[9px] font-bold uppercase truncate px-1 text-gray-300 tracking-tighter">{m['name'].split()[0]}</div>
                            </th>''' for m in members])}
                        </tr>
                    </thead>
                    <tbody class="font-numbers">
    """

    for idx, monat in enumerate(monate_namen):
        html_content += f"""
                        <tr class="border-b border-white/5 hover:bg-white/10 transition-all">
                            <td class="p-1 font-black border-r border-white/10 bg-black/10 text-center text-gray-200 text-[14px] italic tracking-tight">
                                {monat}
                            </td>
        """
        for m in members:
            n_val = m.get("netto_monate", [])[idx] if idx < len(m.get("netto_monate", [])) else 0
            b_val = m.get("brutto_monate", [])[idx] if idx < len(m.get("brutto_monate", [])) else 0

            html_content += f"""
                            <td class="p-1.5 border-r border-white/10 text-center compact-cell font-bold text-[16px]">
                                <span class="val-netto text-netto drop-shadow-[0_2px_4px_rgba(0,0,0,0.8)]">{n_val}</span>
                                <span class="val-brutto text-brutto drop-shadow-[0_2px_4px_rgba(0,0,0,0.8)]">{b_val}</span>
                            </td>
            """
        html_content += "</tr>"

    html_content += """
                        <tr class="bg-white/10 border-t-2 border-white/20">
                            <td class="p-2 font-black border-r border-white/10 text-center text-white uppercase tracking-tighter text-[13px]">
                                TOTAL
                            </td>
    """
    for m in members:
        s_netto = sum(m.get("netto_monate", []))
        s_brutto = sum(m.get("brutto_monate", []))
        is_champ = m['name'] == champion_name

        # Champion Glanz-Effekt
        champ_glow = "drop-shadow-[0_0_15px_rgba(255,255,255,0.4)] scale-110" if is_champ else ""

        html_content += f"""
                            <td class="p-1.5 border-r border-white/10 text-center compact-cell font-black text-[17px]">
                                <span class="val-netto text-netto {champ_glow}">{s_netto}</span>
                                <span class="val-brutto text-brutto {champ_glow}">{s_brutto}</span>
                            </td>
        """

    html_content += """
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="flex gap-6 items-center bg-black/50 px-10 py-3 rounded-full border border-white/10 backdrop-blur-md shadow-lg italic">
                <span id="label-netto" class="uppercase font-black tracking-[0.2em] text-emerald-400 transition-all duration-500 text-sm">Netto-Ansicht</span>
                <span class="text-gray-600 font-thin text-xl">|</span>
                <span id="label-brutto" class="uppercase font-black tracking-[0.2em] text-amber-400 transition-all duration-500 text-sm">Brutto-Ansicht</span>
            </div>

        </div>

        <script>
            const body = document.getElementById('main-body');
            const lNetto = document.getElementById('label-netto');
            const lBrutto = document.getElementById('label-brutto');

            setInterval(() => {
                if (body.classList.contains('mode-netto')) {
                    body.classList.remove('mode-netto');
                    body.classList.add('mode-brutto');
                    lNetto.style.opacity = "0.2";
                    lBrutto.style.opacity = "1";
                } else {
                    body.classList.remove('mode-brutto');
                    body.classList.add('mode-netto');
                    lNetto.style.opacity = "1";
                    lBrutto.style.opacity = "0.2";
                }
            }, 10000);
        </script>
    </body>
    </html>
    """

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Update fertig! Kontrastreiches Cashboard (Grün/Gold) erstellt.")


LOCAL_GIF = "background.gif"
create_champion_website("data.json", LOCAL_GIF)