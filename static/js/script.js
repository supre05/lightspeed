function toggleFields() {
    const userType = document.getElementById('userType').value;
    const individualFields = document.getElementById('individual-fields');
    const organizationFields = document.getElementById('organization-fields');

    individualFields.classList.remove('active');
    organizationFields.classList.remove('active');

    if (userType === 'individual') {
        individualFields.classList.add('active');
    } else if (userType === 'organization') {
        organizationFields.classList.add('active');
    }
}