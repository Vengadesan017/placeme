// document.addEventListener('DOMContentLoaded', function () {
//     fetch('./../api/create-job-form/')
//         .then(response => response.json())
//         .then(data => {
            
//         function appendOptions(dataList, selectId) {
//             const select = document.getElementById(selectId);
//             const existingValues = new Set(Array.from(select.options).map(opt => opt.value));
//             console.log('Total options before:', select.options.length);

//             const fragment = document.createDocumentFragment();
//             dataList.forEach(item => {
//                 if (!existingValues.has(item.id.toString())) {
//                     const option = document.createElement('option');
//                     option.value = item.id;
//                     option.textContent = item.name;
//                     fragment.appendChild(option);
//                 }
//             });
//             select.appendChild(fragment);
//             console.log('Total options After:', select.options.length);

//         }

//             appendOptions(data.locations, 'multi-select-location');
//             appendOptions(data.skills, 'multi-select-skills');
//             appendOptions(data.qualifications, 'multi-select-qualifications');
//             appendOptions(data.benefits, 'multi-select-benefits');

            
//         })
//         .catch(error => {
//             console.error('Error loading dropdown data:', error);
//         });
// });