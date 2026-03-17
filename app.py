import gradio as gr
import httpx
import pandas as pd


def fetch_bitd_data(filter):
    params = {}

    if filter != "All":
        params["conservation_status"] = filter

    r = httpx.get('http://127.0.0.1:8000/species/', params=params)

    data = r.json()
    dataframe = pd.DataFrame(data, columns=['id', 'name', 'scientific_name', 'conservation_status', 'family', 'wingspan_cm'])
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
    gr.Markdown('## Birds Viewer')

    with gr.Tab("Species"):
        with gr.Row():
            with gr.Row():
                filter = gr.Dropdown(
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

                refresh_button = gr.Button('Refresh', scale=1)

        with gr.Row():
            output_birds = gr.Dataframe(
                value=fetch_bitd_data("All"),
                interactive=True
            )

        refresh_button.click(fn=fetch_bitd_data, outputs=output_birds, inputs=filter)

        with gr.Row():
            name = gr.Textbox(label='Name')
            scientific_name = gr.Textbox(label='Scientific Name')

        with gr.Row():
            conservation_status = gr.Textbox(label='Conservation Status')
            filter = gr.Dropdown(
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

            family = gr.Textbox(label='Family')
            filter = gr.Dropdown(
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
            wingspan_cm = gr.Slider(label='WingspaCM', minimum=5, maximum=230)

        with gr.Row():
            create = gr.Button('Create')

        create.click(
            fn=create_species,
            inputs=[name, scientific_name, family, conservation_status, wingspan_cm]
        )

    with gr.Tab("Birds"):
        with gr.Row():
            with gr.Row():
                refresh_button = gr.Button('Refresh')

        with gr.Row():
            output_birds = gr.Dataframe(
                value=feth_birds(),
                interactive=True
            )

        refresh_button.click(fn=feth_birds, outputs=output_birds)

        with gr.Row():
            id = gr.Textbox(label="id")

        with gr.Row():
            nickname = gr.Textbox(label='nickname')
            ring_code = gr.Textbox(label='ring_code')

        with gr.Row():
            age = gr.Number(label="age")
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
            with gr.Row():
                filter = gr.Textbox(label='Filter by observer name', scale=2, interactive=True)
                refresh_button = gr.Button('Refresh', scale=1)

        with gr.Row():
            output_birdsightings = gr.Dataframe(
                value=fetch_birdsightings(""),
                interactive=True
            )

        refresh_button.click(fn=fetch_birdsightings, inputs=filter, outputs=output_birdsightings)

        with gr.Row():
            gr.Markdown('+ Add new sighting')

        with gr.Row():
            bird = gr.Dropdown(label='Bird', choices=get_bird_names(), interactive=True, scale=2)
            refresh_birds = gr.Button('Refresh bird list', scale=1)

        with gr.Row():
            spotted_at = gr.Textbox(label='Spotted at (ISO 8601)', placeholder='e.g. 2024-06-01T09:30:00')
            location = gr.Textbox(label='Location')

        with gr.Row():
            observer = gr.Textbox(label='Observer name')
            notes = gr.Textbox(label='Notes')

        with gr.Row():
            create = gr.Button('Create sighting')

        refresh_birds.click(fn=get_bird_names, outputs=bird)

        create.click(
            fn=create_sighting,
            inputs=[bird, spotted_at, location, observer, notes]
        )

demo.launch(theme=gr.themes.Soft())