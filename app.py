import gradio as gr
import httpx
import pandas as pd




def fetch_bitd_data(filter):
    params = {}

    if filter != "All":
        params["conservation_status"] = filter

    r = httpx.get('http://127.0.0.1:8000/species/', params=params)

    data = r.json()
    dataframe = pd.DataFrame(data, columns=['id', 'name', 'scientific_name','family', 'conservation_status', 'wingspan_cm'])
    return dataframe


def create_species(name, scientific_name, family, conservation_status, wingspan_cm):
    payload = {
        "name": name,
        "scientific_name": scientific_name,
        "family": family,
        "conservation_status": conservation_status,
        "wingspan_cm": wingspan_cm
    }
    httpx.post('http://127.0.0.1:8000/species/', json=payload)


def feth_birds():
    birds_response = httpx.get("http://127.0.0.1:8000/birds/")
    birds_data = birds_response.json()
    birds_df = pd.DataFrame(
        birds_data,
        columns=["id", "nickname", "ring_code", "age", "species_id"]
    )






    species_response = httpx.get("http://127.0.0.1:8000/species/")
    species_data = species_response.json()
    species_df = pd.DataFrame(
        species_data,
        columns=["id", "name"]
    )

    species_df = species_df.rename(columns={"id": "species_id", "name": "species_name"})
    merged_df = birds_df.merge(species_df, on="species_id", how="left")
    merged_df = merged_df[["id", "nickname", "ring_code", "age", "species_name"]]

    return merged_df


def get_species_choices():
    r = httpx.get('http://127.0.0.1:8000/species/')
    species = r.json()
    return [(sp["name"], sp["id"]) for sp in species]


def refresh_species_choices():
    return gr.update(choices=get_species_choices())


def create_bird(nickname, ringCode, age, species):
    payload = {
        "nickname": nickname,
        "ring_code": ringCode,
        "age": age,
        "species": species
    }
    httpx.post('http://127.0.0.1:8000/birds/', json=payload)


def fetch_birdsightings(filter):
    params = {}

    if filter != "":
        params["observer_name"] = filter

    r = httpx.get('http://127.0.0.1:8000/birdspotting/', params=params)
    data = r.json()
    dataframe = pd.DataFrame(
        data,
        columns=['id', 'bird_id', 'spotted_at', 'location', 'observer_name', 'notes']
    )
    return dataframe


def get_bird_names():
    r = httpx.get('http://127.0.0.1:8000/birds/')
    birds = r.json()

    return [(bird["nickname"], bird["id"]) for bird in birds]


def create_sighting(bird, spotted_at, location, observer, notes):
    payload = {
        "bird_id": bird,
        "spotted_at": spotted_at,
        "location": location,
        "observer_name": observer,
        "notes": notes
    }
    httpx.post('http://127.0.0.1:8000/birdspotting/', json=payload)



with gr.Blocks() as demo:
    gr.Markdown('## 🐔 Birds Viewer')
    gr.Markdown('### Live data from the Birds API at http://127.0.0.1:8000')
    

    with gr.Tab("Species"):
        with gr.Row():
            filter = gr.Dropdown(label="Filter by conservation status",
                choices=[
                    "All",
                    "Least Concern",
                    "Near Threatened",
                    "Vulnerable",
                    "Endangered",
                    "Critically Endangered",
                    "Extinct in the Wild",
                    "Extinct"
                ],
                scale=2,
                interactive=True,
                value="All"
            )

            refresh_button = gr.Button('🔄Refresh', scale=1)            

        with gr.Row():
            gr.Markdown('Species')
        with gr.Row():
            output_birds = gr.Dataframe(
                value=fetch_bitd_data("All"),
                interactive=True
            )

        refresh_button.click(fn=fetch_bitd_data, outputs=output_birds, inputs=filter)
        with gr.Accordion("+ Add new species"):
            with gr.Row():
                name = gr.Textbox(placeholder="e.g. Atlantic Puffin", label='Name')
                scientific_name = gr.Textbox(placeholder="e.g. Fratercula arctica", label='Scientific Name')

            with gr.Row():
                family = gr.Textbox(placeholder= "e.g. Alcidae", label='Family')
                conservation_status = gr.Dropdown( label="conservation_status",
                    choices=[
                        "Least Concern",
                        "Near Threatened",
                        "Vulnerable",
                        "Endangered",
                        "Critically Endangered",
                        "Extinct in the Wild",
                        "Extinct"
                    ],
                    scale=2,
                    interactive=True
                )


                
                wingspan_cm = gr.Slider(label='Wingspan (cm)', minimum=0, maximum=300)

            with gr.Row():
                create = gr.Button('Create species')

            create.click(
                fn=create_species,
                inputs=[name, scientific_name, family, conservation_status, wingspan_cm]
            )

    with gr.Tab("Birds"):
        with gr.Row():
            with gr.Row():
                refresh_button = gr.Button('🔄Refresh')
        with gr.Row():
            gr.Markdown('Birds')
        with gr.Row():
            output_birds = gr.Dataframe(
                value=feth_birds(),
                interactive=True
            )

        refresh_button.click(fn=feth_birds, outputs=output_birds)
        with gr.Accordion("+ Add new species"):
            with gr.Row():
                nickname = gr.Textbox(placeholder="e.g. Skipper", label='nickname')
                ring_code = gr.Textbox(placeholder="e.g. AB-1234", label='ring_code')

            with gr.Row():
                age = gr.Number(placeholder=int(0),label="age")
                species = gr.Dropdown(label="species", choices=get_species_choices(), interactive=True)

            with gr.Row():
                refresh_species_btn = gr.Button("🔄 Refresh species list", scale=1)
                create_bird_btn = gr.Button("Create bird", variant="primary", scale=2)

            refresh_species_btn.click(fn=refresh_species_choices, outputs=species)

            create_bird_btn.click(
                fn=create_bird,
                inputs=[nickname, ring_code, age, species]
            )

    with gr.Tab("Birdspotting"):
        with gr.Row():
            filter = gr.Textbox(placeholder="e.g. Jane", label='Filter by observer name', scale=2, interactive=True)
            refresh_button = gr.Button('🔄Refresh', scale=1)



        with gr.Row():
            output_birdsightings = gr.Dataframe(
                value=fetch_birdsightings(""),
                interactive=True
            )
        refresh_button.click(fn=fetch_birdsightings, inputs=filter, outputs=output_birdsightings)

        with gr.Accordion('+ Add new sighting'):

            with gr.Row():
                bird = gr.Dropdown(label='Bird', choices=get_bird_names(), interactive=True, scale=2)
                refresh_birds = gr.Button('🔄Refresh bird list', scale=1)
            refresh_birds.click(fn=get_bird_names, outputs=bird)

            with gr.Row():
                spotted_at = gr.Textbox(label='Spotted at (ISO 8601)', placeholder='e.g. 2024-06-01T09:30:00')
                location = gr.Textbox(placeholder="e.g. Cliffs of Moher", label='Location')

            with gr.Row():
                observer = gr.Textbox(placeholder= "e.g. Jane Doe", label='Observer name')
                notes = gr.Textbox(placeholder="e.g. Flying low over the water", label='Notes(optional)')

            with gr.Row():
                create = gr.Button('Create sighting')


            create.click(
                fn=create_sighting,
                inputs=[bird, spotted_at, location, observer, notes]
            )






    with gr.Tab("Feedack =)"):
            gr.Markdown("✨👍😊 Your feedback 😊👍✨")
            star_rating = gr.HTML(
                value=3, 
                html_template="""
                <h2>Star Rating:</h2>
                ${Array.from({length: 5}, (_, i) => `<img class='${i < value ? '' : 'faded'}' src='https://upload.wikimedia.org/wikipedia/commons/d/df/Award-star-gold-3d.svg'>`).join('')}
                <button id='submit-btn'>Submit Rating✨</button>
                """, 
                css_template="""
                    img { height: 50px; display: inline-block; cursor: pointer; }
                    .faded { filter: grayscale(100%); opacity: 0.3; }
                """,
                js_on_load="""
                    const imgs = element.querySelectorAll('img');
                    imgs.forEach((img, index) => {
                        img.addEventListener('click', () => {
                            props.value = index + 1;
                        });
                    });
                    const submitBtn = element.querySelector('#submit-btn');
                    submitBtn.addEventListener('click', () => {
                        trigger('submit');
                    });
                """)
            rating_output = gr.Textbox(label="Submitted Rating :3")
            star_rating.submit(lambda x: x, inputs=star_rating, outputs=rating_output)
            gr.HTML('<img src="https://media1.tenor.com/m/6yXFJh70KTYAAAAd/%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%BD%D1%8B%D0%B9%D0%BC%D0%B0%D0%BB%D1%8C%D1%87%D0%B8%D0%BA%D0%B2%D0%BC%D0%B0%D1%81%D0%BA%D0%B5%D1%82%D0%B0%D0%BD%D1%86%D1%83%D0%B5%D1%82%D1%82%D0%B8%D0%BA%D1%82%D0%BE%D0%BAa.gif" width="400">')

demo.launch(theme=gr.themes.Soft(primary_hue=gr.themes.colors.blue, secondary_hue=gr.themes.colors.blue, font=[gr.themes.GoogleFont("Inconsolata"), "Arial", "sans-serif"]))