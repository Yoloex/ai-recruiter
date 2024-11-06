import json
import time
import gradio as gr
from interviewer.interviewer import Interviewer
from interviewer.preprocessor import extract_requirement

with open("data/recruiter-preset.txt", "r") as f:
    PRESETS = f.read()

with open("data/examples/airbnb.json") as f:
    data = json.loads(f.read())

with open(
    "data/jobs/{}".format(data["Job Description"]), "r", encoding="utf-8"
) as f:
    job = f.read()


class Interview:
    def __init__(self):
        self.ui = self.create_ui()
        self.interviewer = Interviewer()
        self.done = False
        self.preset = None

    def create_ui(self):
        with gr.Blocks() as demo:

            gr.Markdown("# AI Interview Agent")

            with gr.Row():
                with gr.Column(min_width=1000):
                    with gr.Row():
                        company = gr.Textbox(
                            data["Company"],
                            placeholder="Enter the company's name",
                            label="Company",
                        )
                        position = gr.Textbox(
                            data["Job Title"],
                            placeholder="Enter the job title",
                            label="Job Title",
                            max_length=100,
                        )
                    with gr.Row():
                        jd = gr.TextArea(
                            job,
                            placeholder="Enter the job description",
                            label="Job Description",
                            lines=5,
                            max_lines=5,
                        )
                with gr.Column(min_width=300):
                    mission = gr.TextArea(
                        data["Mission"],
                        placeholder="Enter the company's mission",
                        label="Company's Mission",
                        lines=3,
                        max_lines=3,
                    )
                    value = gr.TextArea(
                        data["Core Values"],
                        placeholder="Enter the company's value",
                        label="Company' Core Values",
                        lines=3,
                        max_lines=3,
                    )

                start = gr.Button("Start Interview")

            with gr.Blocks():
                self.chatbot = gr.Chatbot(type="messages", height=300)
                self.chatbot.change(self.talking, None, self.chatbot)
                clear = gr.Button("Clear")

                start.click(
                    self.preprocess, [company, position, mission, value, jd]
                ).then(self.talking, None, self.chatbot)

                clear.click(
                    self.close,
                    None,
                    self.chatbot,
                    queue=False,
                )

        return demo

    def preprocess(self, company, position, mission, value, job_description):
        gr.Info("Extracting requirements ...", duration=6)

        requirements = extract_requirement(job_description)

        self.preset = PRESETS.format(
            company=company,
            position=position,
            mission=mission,
            requirements=requirements,
            value=value,
        )

        self.interviewer.set_preset(self.preset)
        gr.Info("Requirements extracted!", duration=2)

    def talking(self):

        while not self.done:
            gr.Info("Your turn. Say please", duration=2)
            time.sleep(1)

            user_speech = self.interviewer.stt()
            gr.Info("Your speech is accepted. Responding ...")

            if user_speech.strip(
                " "
            ).lower() == "i am done." or self.interviewer.is_done(user_speech):
                self.done = True

            self.interviewer.history.append({"role": "user", "content": user_speech})

            response = self.interviewer.response()

            self.interviewer.history.append(
                {"role": "assistant", "content": response}
            )

            self.interviewer.tts(response)

            return self.interviewer.history

        return self.interviewer.history

    def close(self):
        self.interviewer.audio_processor.close()
        self.interviewer.set_preset(self.preset)

        return []


if __name__ == "__main__":
    mock = Interview()
    mock.ui.launch()
