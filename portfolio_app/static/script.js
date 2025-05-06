function addSkillField() {
  const wrapper = document.getElementById('skills-wrapper');
  const input = document.createElement('input');
  input.name = "skills";
  input.type = "text";
  input.className = "skill-input block w-full p-2.5 text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300";
  input.placeholder = "e.g., JavaScript";
  wrapper.appendChild(input);
}

function addProjectField() {
  const wrapper = document.getElementById('project-wrapper');
  const projectGroup = document.createElement('div');
  projectGroup.className = "project-group mt-6 border-t pt-4";

  projectGroup.innerHTML = `
    <label class="block mb-2 font-medium">Project Title</label>
    <input name="project_title" type="text" class="block w-full p-2 border rounded" placeholder="e.g., Budget Tracker" />

    <label class="block mt-4 mb-2 font-medium">Description</label>
    <textarea name="project_description" rows="3" class="block w-full p-2 border rounded" placeholder="What does the project do?"></textarea>

    <label class="block mt-4 mb-2 font-medium">GitHub Link</label>
    <input name="project_github" type="url" class="block w-full p-2 border rounded" placeholder="https://github.com/..." />
  `;
  wrapper.appendChild(projectGroup);
}