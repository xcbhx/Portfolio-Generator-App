function addSkillField() {
  const wrapper = document.getElementById('skills-wrapper');
  const input = document.createElement('input');
  input.name = "skills";
  input.type = "text";
  input.className = "skill-input block w-full p-2.5 text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300";
  input.placeholder = "e.g., JavaScript";
  wrapper.appendChild(input);
}