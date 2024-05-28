const container=document.querySelector('#container');
const singnInButton=document.querySelector('#singnIn');
const singnUpButton=document.querySelector('#singnUp');

singnUpButton.addEventListener('click',()=>container.classList.add('right-panel-active'))
singnInButton.addEventListener('click',()=>container.classList.remove('right-panel-active'))