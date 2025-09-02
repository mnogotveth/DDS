(function(){
  function qs(sel, root){ return (root||document).querySelector(sel); }
  function createOption(v, t){ const o=document.createElement('option'); o.value=v; o.textContent=t; return o; }
  function setOptions(selectEl, list, selected){
    selectEl.innerHTML = '';
    selectEl.appendChild(createOption('', '---------'));
    list.forEach(it => selectEl.appendChild(createOption(it.id, it.name)));
    if (selected) selectEl.value = String(selected);
  }

  //форма создания/редактирования
  function initFormCascade(){
    const typeSel = qs('#id_type');
    const catSel  = qs('#id_category');
    const subSel  = qs('#id_subcategory');
    if(!typeSel || !catSel || !subSel) return;

    async function loadCategories(typeId, selectedCat){
      if(!typeId){ setOptions(catSel, [], ''); setOptions(subSel, [], ''); return; }
      const res = await fetch(`/api/types/${typeId}/categories/`);
      const data = await res.json();
      setOptions(catSel, data, selectedCat);
      if(!selectedCat){ setOptions(subSel, [], ''); }
    }
    async function loadSubcategories(catId, selectedSub){
      if(!catId){ setOptions(subSel, [], ''); return; }
      const res = await fetch(`/api/categories/${catId}/subcategories/`);
      const data = await res.json();
      setOptions(subSel, data, selectedSub);
    }

    typeSel.addEventListener('change', () => loadCategories(typeSel.value, null));
    catSel.addEventListener('change', () => loadSubcategories(catSel.value, null));

    // для режима редактирования: если value уже есть — восстановить каскад
    if(typeSel.value){
      const selectedCat = catSel.getAttribute('value') || catSel.value;
      const selectedSub = subSel.getAttribute('value') || subSel.value;
      loadCategories(typeSel.value, selectedCat).then(()=>{
        if(selectedCat){ loadSubcategories(selectedCat, selectedSub); }
      });
    }
  }

  //фильтры на списке 
  async function initFiltersCascade(){
    const typeF = qs('#flt_type');
    const catF  = qs('#flt_category');
    const subF  = qs('#flt_subcategory');
    if(!typeF || !catF || !subF) return;

    const defaults = window.UI_FILTER_DEFAULTS || {};

    async function loadCategories(typeId, selected){
      if(!typeId){ setOptions(catF, [], ''); setOptions(subF, [], ''); return; }
      const r = await fetch(`/api/types/${typeId}/categories/`);
      setOptions(catF, await r.json(), selected || '');
      if(!selected){ setOptions(subF, [], ''); }
    }
    async function loadSubcategories(catId, selected){
      if(!catId){ setOptions(subF, [], ''); return; }
      const r = await fetch(`/api/categories/${catId}/subcategories/`);
      setOptions(subF, await r.json(), selected || '');
    }

    typeF.addEventListener('change', () => loadCategories(typeF.value, null));
    catF.addEventListener('change', () => loadSubcategories(catF.value, null));

    if(typeF.value || defaults.type){
      const t = typeF.value || defaults.type;
      await loadCategories(t, defaults.category || '');
      if(defaults.category){
        await loadSubcategories(defaults.category, defaults.subcategory || '');
      }
    }
  }

  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', () => { initFormCascade(); initFiltersCascade(); });
  } else {
    initFormCascade(); initFiltersCascade();
  }
})();
