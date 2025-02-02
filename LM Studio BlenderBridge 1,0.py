bl_info = {
    "name": "Blender Scripting AI for LM Studio Server",
    "blender": (4, 2, 0),
    "category": "Development",
    "author": "Sondre Ileby",
    "version": (1, 0),
    "description": "Integrates Blender with a chat assistant API to get responses and execute scripts.",
    "support": "COMMUNITY",
    "tracker_url": "https://www.blender.org/support/",
}

import bpy
import requests
import subprocess
import re

# Function to send the request to the API and handle the response
def generate_chat_response(localhost_numbers, model, system_prompt, prompt, include_last_response):
    # URL using the localhost number for the API endpoint
    url = f"http://localhost:{localhost_numbers}/v1/chat/completions"  # Updated URL format
    
    # If "include_last_response" is checked, append the last response
    if include_last_response:
        prompt = f"{prompt}\n{system_prompt}"

    # Define the chat messages (conversation history)
    data = {
        "model": model,  # Specify the model
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "config": {
            "gpuOffload": "max"  # Optional: GPU offloading
        }
    }

    # Send POST request to the server
    response = requests.post(url, json=data)

    if response.status_code == 200:
        response_data = response.json()
        assistant_response = response_data.get("choices", [{}])[0].get("message", {}).get("content", "No response")
        
        # Print the assistant's response to the Blender console
        print("Assistant's response:", assistant_response)

        # Create a new text block in Blender to store the response
        text_block = bpy.data.texts.new(f"AI_{prompt}")
        text_block.write(assistant_response)

        # Copy the response to the Mac clipboard using pbcopy (macOS only)
        subprocess.run("pbcopy", input=assistant_response, text=True)
        print("Response copied to clipboard!")
    else:
        print(f"Request failed with status code: {response.status_code}")

# Panel class to display the UI in the N-panel (sidebar)
class AIChatPanel(bpy.types.Panel):
    """Creates a Panel in the N-panel (sidebar) to trigger the chat response generation."""
    bl_label = "Step 1. Load model in LM Studio"
    bl_idname = "VIEW3D_PT_ai_chat"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'LMStudioAI'  # Custom tab name for the N-panel

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Create input fields for localhost numbers, model, system prompt, prompt
        layout.prop(scene, "ai_localhost_numbers")
        layout.prop(scene, "ai_model")
        layout.prop(scene, "ai_system_prompt")
        layout.prop(scene, "ai_prompt")
        layout.prop(scene, "ai_include_last_response")

        # Add a button to generate the response
        layout.operator("wm.generate_ai_response", text="Get AI Response")

        # Add a button to run the generated script
        layout.operator("wm.run_ai_script", text="Run Script")

# Operator to handle the button click and call the API function
class GenerateAIResponseOperator(bpy.types.Operator):
    """Operator to send a request to the AI API and handle the response."""
    bl_idname = "wm.generate_ai_response"
    bl_label = "Generate AI Response"
    
    def execute(self, context):
        # Call the function that sends the request to the API with values from the panel
        scene = context.scene
        generate_chat_response(
            scene.ai_localhost_numbers,
            scene.ai_model,
            scene.ai_system_prompt,
            scene.ai_prompt,
            scene.ai_include_last_response
        )
        return {'FINISHED'}

class RunAIScriptOperator(bpy.types.Operator):
    """Operator to execute the script from the generated AI response."""
    bl_idname = "wm.run_ai_script"
    bl_label = "Run AI Script"

    def execute(self, context):
        # Get the text block created from the AI response
        scene = context.scene
        text_block = bpy.data.texts.get(f"AI_{scene.ai_prompt}")

        if text_block:
            # Get the response as a string
            text_response = text_block.as_string()

            # Clean up the response: remove code block markers (```)
            text_response = re.sub(r'^```(.*)```$', r'\1', text_response, flags=re.DOTALL | re.MULTILINE)

            # Only apply these changes to lines 1-6
            lines = text_response.splitlines()

            # Apply substitutions only if these lines exist
            for i in range(min(6, len(lines))):  # Process first 6 lines
                # Comment out lines with .delete, .remove, .select or .select_by_type
                lines[i] = re.sub(r'^.*\.delete.*$', r'# \g<0>', lines[i], flags=re.IGNORECASE | re.MULTILINE)
                lines[i] = re.sub(r'^.*\.remove.*$', r'# \g<0>', lines[i], flags=re.IGNORECASE | re.MULTILINE)
                lines[i] = re.sub(r'^.*\.select.*$', r'# \g<0>', lines[i], flags=re.IGNORECASE | re.MULTILINE)
                lines[i] = re.sub(r'^.*\.select_by_type.*$', r'# \g<0>', lines[i], flags=re.IGNORECASE | re.MULTILINE)

            # Rebuild the cleaned-up response
            cleaned_response = "\n".join(lines)
            # Write the cleaned-up response back into the text block
            text_block.clear()  # Clear the existing content in the text block
            text_block.write(cleaned_response)  # Write the cleaned-up content

            # Create a function to set the active text block and execute the script with a delay
            def set_active_text():
                # Set the active text editor to the current text block
                for area in bpy.context.screen.areas:
                    if area.type == 'TEXT_EDITOR':
                        area.spaces.active.text = text_block

                try:
                    # Try executing the cleaned-up script
                    exec(cleaned_response, globals())  # Execute the cleaned response as Python code

                    # Provide a success message if execution works
                    self.report({'INFO'}, "Executed successfully in Scripting tab")
                except SyntaxError as e:
                    # Detailed error handling for syntax errors
                    self.report({'ERROR'}, f"SyntaxError: {e.msg} in script.")
                    print(f"SyntaxError: {e.msg} in script.")
                except Exception as e:
                    # Capture any other errors
                    self.report({'ERROR'}, f"Error executing script: {e}")
                    print(f"Error executing script: {e}")

            # Register the timer to call the function with a delay (0.1 seconds)
            bpy.app.timers.register(set_active_text, first_interval=0.1)
        else:
            self.report({'ERROR'}, "No script to execute!")
            print("No script to execute!")

        return {'FINISHED'}
        
# Add custom properties to the scene for user input
def add_custom_properties():
    bpy.types.Scene.ai_localhost_numbers = bpy.props.IntProperty(
        name="Localhost Number",
        default=1234,
        description="The localhost number to send requests to"
    )
    bpy.types.Scene.ai_model = bpy.props.StringProperty(
        name="Model",
        default="blenderllm-7.6b_gguf",
        description="The model to use for AI responses"
    )
    bpy.types.Scene.ai_system_prompt = bpy.props.StringProperty(
        name="System Prompt",
        default="You are a helpful assistant.",
        description="The system message to guide the AI's behavior"
    )
    bpy.types.Scene.ai_prompt = bpy.props.StringProperty(
        name="Prompt",
        default="What is the meaning of life?",
        description="The user's message to the AI"
    )
    bpy.types.Scene.ai_include_last_response = bpy.props.BoolProperty(
        name="Include Last Response",
        default=False,
        description="Include the last AI response in the current prompt"
    )

# Registering the classes (panel and operator)
def register():
    add_custom_properties()
    bpy.utils.register_class(AIChatPanel)
    bpy.utils.register_class(GenerateAIResponseOperator)
    bpy.utils.register_class(RunAIScriptOperator)

# Unregistering the classes
def unregister():
    bpy.utils.unregister_class(AIChatPanel)
    bpy.utils.unregister_class(GenerateAIResponseOperator)
    bpy.utils.unregister_class(RunAIScriptOperator)
    del bpy.types.Scene.ai_localhost_numbers
    del bpy.types.Scene.ai_model
    del bpy.types.Scene.ai_system_prompt
    del bpy.types.Scene.ai_prompt
    del bpy.types.Scene.ai_include_last_response

# Addon entry point
if __name__ == "__main__":
    register()
