# Blender Scripting AI for LM Studio Server

This Blender addon integrates Blender with a chat assistant API to get responses and execute scripts directly in Blender. You can interact with the AI assistant, ask questions, and execute generated Python scripts within Blender.

![BlenderAI13](https://raw.githubusercontent.com/SurgeonTalus/Blender-Scripting-AI-for-LM-Studio-Server/main/LM%20Studio%20BlenderBridge%20Images/BlenderAI13.png)

## Features

- **API Integration**: Communicate with an AI assistant via an API running on your local server.
- **AI Response**: Get answers from the AI and generate executable Blender Python scripts.
- **Blender Integration**: Automatically save AI responses as text blocks in Blender and run the generated scripts.

## Requirements

- **Blender 4.2 or higher**
- **LM Studio Server** running locally
- Python `requests` library for making API calls.

## Installation

1. **Download the Addon**:
   - Go to the [releases section](https://github.com/SurgeonTalus/Blender-Scripting-AI-for-LM-Studio-Server/releases) of the repository.
   - Download the `.zip` file of the addon.

2. **Install the Addon in Blender**:
   - Open **Blender**.
   - Go to the **Edit** menu in the top bar and select **Preferences**.
   - In the **Preferences** window, go to the **Add-ons** tab.
   - Click the **Install...** button at the top-right of the Add-ons panel.
   - Locate the `.zip` file you downloaded and click **Install Add-on**.
   - Once installed, find the addon in the list of available addons and enable it by checking the checkbox next to its name.

3. **Using the Addon**:
   - After enabling the addon, go to the **3D Viewport**.
   - Open the **N-panel** (press `N` on your keyboard).
   - You will find a new tab named **LMStudioAI**.
   - Inside this tab, you can enter the necessary parameters like the model, system prompt, and user prompt, and then click **Get AI Response** to interact with the AI.


## How to Use

1. **Step 1**: Load your model in LM Studio.
2. **Step 2**: Open the N-panel in Blender (on the right side of the 3D Viewport).
3. **Step 3**: Enter the following fields:
   - **Localhost Number**: The port number of your local server.
   - **Model**: Choose the AI model you want to use.
   - **System Prompt**: The initial instruction for the AI.
   - **Prompt**: Ask the AI a question or give it a task.
   - **Include Last Response**: If checked, include the last AI response in the new prompt.

4. **Step 4**: Click the **"Get AI Response"** button to generate the response.
5. **Step 5**: To execute the script, click **"Run Script"**.

The AI will provide a response that can be executed as Python code in Blender, making it easy to automate tasks within Blender.

## Screenshots

Here are some images showing the interface and how it works:

![BlenderAI11](https://github.com/SurgeonTalus/Blender-Scripting-AI-for-LM-Studio-Server/blob/main/LM%20Studio%20BlenderBridge%20Images/BlenderAI11.png)
![BlenderAI12](https://raw.githubusercontent.com/SurgeonTalus/Blender-Scripting-AI-for-LM-Studio-Server/main/LM%20Studio%20BlenderBridge%20Images/BlenderAI12.png)

![BlenderAI14](https://raw.githubusercontent.com/SurgeonTalus/Blender-Scripting-AI-for-LM-Studio-Server/main/LM%20Studio%20BlenderBridge%20Images/BlenderAI14.png)

**Image Series**: BlenderAI11 through BlenderAI14 show the AI responses and how they integrate with Blender.

## Code Explanation

- **Blender Integration**: A custom panel is added to Blender’s UI where you can input various parameters to interact with the AI.
- **API Request**: The addon sends your prompt to the AI server running locally and retrieves the response.
- **Script Execution**: The AI's response is processed and can be executed directly as a script in Blender's scripting tab.
## Bugs
Does not clean out text that is not python code.
Sometimes python is written after ´´´python. import bpy Should be start of code. 
Needs regex modifier to include text in between ''' only.py
## License

This project is open-source and licensed under the MIT License.
