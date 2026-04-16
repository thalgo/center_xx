import json


def create_champion_website(json_file, gif_url):
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
        <title>Team Cashboard Center</title>
        <style>
            body {{
                background-image: url('{gif_url}');
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
                margin: 0;
                overflow: hidden;
            }}
            .bg-overlay {{ 
                background-color: rgba(0, 0, 0, 0.75); 
                height: 100vh; 
                width: 100vw; 
                display: flex;
                flex-direction: column;
                justify-content: center; 
                align-items: center;     
            }}

            .compact-cell {{ width: calc(100vw / 27); min-width: 0; }}

            .mode-netto .val-brutto {{ display: none; }}
            .mode-brutto .val-netto {{ display: none; }}

            .val-netto, .val-brutto {{
                animation: fadeIn 0.5s ease-in-out;
            }}

            @keyframes fadeIn {{
                from {{ opacity: 0; transform: scale(0.9); }}
                to {{ opacity: 1; transform: scale(1); }}
            }}

            /* Kronen-Styling - Position angepasst */
            .crown {{
                position: absolute;
                top: 0px; 
                left: 40%;
                transform: translateX(-50%) rotate(-15deg);
                font-size: 18px;
                color: #f59e0b;
                text-shadow: 0 0 12px rgba(245, 158, 11, 0.9), 0 0 3px rgba(0,0,0,1);
                z-index: 50;
                pointer-events: none;
            }}
        </style>
    </head>
    <body class="text-white font-sans mode-netto" id="main-body">
        <div class="bg-overlay p-4">

            <header class="mb-6">
                <h1 class="text-5xl font-black uppercase tracking-[0.5em] text-emerald-400 drop-shadow-[0_0_20px_rgba(52,211,153,0.6)] text-center">
                    Cashboard Center XX / VI
                </h1>
            </header>

            <div class="w-[98vw] bg-black/40 backdrop-blur-3xl rounded-xl border border-white/10 shadow-2xl overflow-hidden mb-8">
                <table class="w-full table-fixed border-collapse">
                    <thead>
                        <tr class="bg-white/10">
                            <th class="w-20 pt-5 pb-2 border-r border-white/10 uppercase font-bold text-gray-500 text-[10px]">Monat</th>
                            {" ".join([f'''
                            <th class="pt-5 pb-1 border-r border-white/10 text-center compact-cell relative">
                                {'<div class="crown">👑</div>' if m['name'] == champion_name else ''}
                                <img src="https://ui-avatars.com/api/?name={m['name'].replace(" ", "+")}&background=random&color=fff&size=40" 
                                     class="w-7 h-7 rounded-full mx-auto mb-1 border border-white/20 shadow-sm relative z-0">
                                <div class="text-[8px] font-bold uppercase truncate px-1 text-gray-300">{m['name'].split()[0]}</div>
                            </th>''' for m in members])}
                        </tr>
                    </thead>
                    <tbody>
    """

    for idx, monat in enumerate(monate_namen):
        html_content += f"""
                        <tr class="border-b border-white/5 hover:bg-white/5 transition-all">
                            <td class="p-1 font-bold border-r border-white/10 bg-black/20 text-center text-gray-400 text-[11px]">
                                {monat[:3]}
                            </td>
        """
        for m in members:
            n_val = m.get("netto_monate", [])[idx] if idx < len(m.get("netto_monate", [])) else 0
            b_val = m.get("brutto_monate", [])[idx] if idx < len(m.get("brutto_monate", [])) else 0

            html_content += f"""
                            <td class="p-1.5 border-r border-white/10 text-center compact-cell font-black text-[14px]">
                                <span class="val-netto text-emerald-300 drop-shadow-sm">{n_val}</span>
                                <span class="val-brutto text-amber-400 drop-shadow-sm">{b_val}</span>
                            </td>
            """
        html_content += "</tr>"

    html_content += """
                        <tr class="bg-white/5 border-t-2 border-white/20">
                            <td class="p-2 font-black border-r border-white/10 text-center text-white uppercase tracking-tighter text-[12px]">
                                TOTAL
                            </td>
    """
    for m in members:
        s_netto = sum(m.get("netto_monate", []))
        s_brutto = sum(m.get("brutto_monate", []))
        is_champ = m['name'] == champion_name
        total_class_n = "text-emerald-400 drop-shadow-[0_0_8px_rgba(52,211,153,0.6)]" if is_champ else "text-emerald-400"
        total_class_b = "text-amber-500 drop-shadow-[0_0_8px_rgba(245,158,11,0.6)]" if is_champ else "text-amber-500"

        html_content += f"""
                            <td class="p-1.5 border-r border-white/10 text-center compact-cell font-black text-[15px]">
                                <span class="val-netto {total_class_n}">{s_netto}</span>
                                <span class="val-brutto {total_class_b}">{s_brutto}</span>
                            </td>
        """

    html_content += """
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="flex gap-6 items-center bg-black/60 px-10 py-3 rounded-full border border-white/10 backdrop-blur-md shadow-lg">
                <span id="label-netto" class="uppercase font-black tracking-[0.2em] text-emerald-400 transition-all duration-500 text-sm">Netto</span>
                <span class="text-gray-600 font-thin text-xl">|</span>
                <span id="label-brutto" class="uppercase font-black tracking-[0.2em] text-amber-500 opacity-20 transition-all duration-500 text-sm">Brutto</span>
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
    print(f"Update fertig! Champion: {champion_name} hat nun genug Platz für die Krone.")


GIF_URL = "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExaG44eXVpMHh1c2xvbnA4bGUydHA5MWZydXE0djIzYTkwaG8wc281MiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/JpG2A9P3dPHXaTYrwu/giphy.gif"
create_champion_website("data.json", GIF_URL)