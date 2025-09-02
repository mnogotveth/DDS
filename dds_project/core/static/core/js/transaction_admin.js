(function(){
  function $(sel){ return document.querySelector(sel); }
  function createOption(v, t){ const o=document.createElement('option'); o.value=v; o.textContent=t; return o; }

  function populate(url, selectEl, selected){
    fetch(url)
      .then(r => r.json())
      .then(data => {
        selectEl.innerHTML = '';
        selectEl.appendChild(createOption('', '---------'));
        data.forEach(it => selectEl.appendChild(createOption(it.id, it.name)));
        if (selected) selectEl.value = String(selected);
        const evt = new Event('change', { bubbles: true });
        selectEl.dispatchEvent(evt);
      });
  }

  function init(){
    const typeSel = $('#id_type');
    const catSel = $('#id_category');
    const subSel = $('#id_subcategory');
    if(!typeSel || !catSel || !subSel) return;

    const currentType = typeSel.value;
    const currentCategory = catSel.value;
    const currentSubcategory = subSel.value;

    typeSel.addEventListener('change', function(){
      const typeId = this.value;
      if(!typeId){
        catSel.innerHTML = '<option value="">---------</option>';
        subSel.innerHTML = '<option value="">---------</option>';
        return;
      }
      populate(`/api/types/${typeId}/categories/`, catSel, null);
      subSel.innerHTML = '<option value="">---------</option>';
    });

    catSel.addEventListener('change', function(){
      const catId = this.value;
      if(!catId){
        subSel.innerHTML = '<option value="">---------</option>';
        return;
      }
      populate(`/api/categories/${catId}/subcategories/`, subSel, null);
    });

    if(currentType){
      populate(`/api/types/${currentType}/categories/`, catSel, currentCategory);
      if(currentCategory){
        populate(`/api/categories/${currentCategory}/subcategories/`, subSel, currentSubcategory);
      }
    }
  }

  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
