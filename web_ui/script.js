document.addEventListener('DOMContentLoaded', () => {
    const taskInput = document.getElementById('taskInput');
    const runTaskBtn = document.getElementById('runTaskBtn');
    const taskOutput = document.getElementById('taskOutput');

    runTaskBtn.addEventListener('click', async () => {
        const taskDescription = taskInput.value.trim();
        if (!taskDescription) {
            alert('Please enter a programming task.');
            return;
        }

        taskOutput.textContent = 'Processing task...';
        runTaskBtn.disabled = true;

        // Simulate API call to the Tanuki-Programmer backend
        // In a real application, this would be a fetch() call to your Python backend
        // For demonstration, we'll simulate a delay and a response.
        try {
            const response = await simulateBackendCall(taskDescription);
            taskOutput.textContent = response;
        } catch (error) {
            taskOutput.textContent = `Error: ${error.message}`;
        } finally {
            runTaskBtn.disabled = false;
        }
    });

    function simulateBackendCall(task) {
        return new Promise(resolve => {
            setTimeout(() => {
                const simulatedResponse = `
Task: "${task}"

---
Simulated Tanuki-Programmer Output:

Analyzing task requirements...
Breaking down into sub-tasks...
Generating code for main logic...
Running tests...
Refactoring for production quality...

Task completed successfully!
(This is a simulated response. Actual output will vary based on the task and Tanuki-Programmer's capabilities.)
                `;
                resolve(simulatedResponse);
            }, 2000); // Simulate a 2-second delay
        });
    }
});
