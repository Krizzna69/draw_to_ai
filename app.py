import streamlit as st
import requests
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io
import google.generativeai as genai

genai.configure(api_key="AIzaSyAawh0tRqyCOsyz7x9GxVbV_tkUzBsZ59s")

# Function to generate a short story from an image using Gemini 1.5
def generate_stry(image_path, age_group="5-8", language='en'):
    # Open the image file
    image = Image.open(image_path)

    # Generate content using Gemini model
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        [
            f"Write a short, fun, and imaginative story for a {age_group}-year-old kid based on this image. "
            "Make it engaging, age-appropriate, and full of wonder. "
            "Focus on creativity and a clear beginning, middle, and end. "
            "Avoid using complex words or phrases. "
            "The story should be easy to understand and enjoyable for children.",
            f"And generate the text in {language}",
            image,
        ]
    )

    # Return the generated story
    return response.text


# Main function for Streamlit app
def main():
    st.title("🎨 Draw and Generate Image with Story App")
    st.write("Draw your sketch, provide a description, and generate a creative story based on the image!")

    # Create a drawable canvas for sketching
    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 1)",  # Fixed fill color with opacity
        stroke_width=2,  # Width of brush strokes
        stroke_color="#000000",  # Default brush color
        background_color="#FFFFFF",  # Background color
        width=512,
        height=512,
        drawing_mode="freedraw",  # Mode to draw freely
        key="canvas",
    )

    # Input for age group
    age_group = st.selectbox("Select the Age Group for the Story", ["5-8", "9-12", "13-16"])

    # Input for language
    language = st.selectbox("Select Language", ["en", "es", "fr", "de"])

    # Generate button
    if st.button("Generate Image and Story"):
        if canvas_result.image_data is None:
            st.warning("Please draw something on the canvas!")
        else:
            with st.spinner("Generating your image and story... Please wait."):

                # Convert the canvas image to bytes
                image = Image.fromarray((canvas_result.image_data[:, :, :3] * 255).astype("uint8"))
                image_bytes = io.BytesIO()
                image.save(image_bytes, format="PNG")
                image_bytes.seek(0)

                # Save the drawn image temporarily
                temp_image_path = "../user_drawn_image.png"
                image.save(temp_image_path)

                # Generate the story using the generate_stry function
                story = generate_stry(temp_image_path, age_group=age_group, language=language)

                # Show the generated story
                st.subheader("Generated Story Based on the Image:")
                st.write(story)

                # Show the drawn image
                st.subheader("Your Drawn Image:")
                st.image(image, caption="Your Sketch", use_column_width=True)


if __name__ == "__main__":
    main()
