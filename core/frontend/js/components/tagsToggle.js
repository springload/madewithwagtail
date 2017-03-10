/**
 * Toggles the visibility of the whole tag list.
 * By default only a subset of all tags is shown.
 */
const toggleTagsVisibility = (tagsContainer, e) => {
    const tagsToggle = e.target;
    const wasVisible = JSON.parse(tagsToggle.getAttribute('aria-expanded'));
    const isVisible = !wasVisible;
    tagsToggle.setAttribute('aria-expanded', isVisible);
    tagsContainer.setAttribute('aria-hidden', !isVisible);

    // First toggle hide/show in the inner element, then toggle the animation.
    tagsContainer.children[0].classList.toggle('u-hide', !isVisible);
    tagsContainer.classList.toggle('tags__additional--show', isVisible)
    tagsToggle.innerHTML = isVisible ? 'Show fewer tags' : 'Show more tags';
};

export default {
    init() {
        const tagsToggle = document.querySelector('[data-tags-toggle]');
        const tagsContainer = document.querySelector('[data-tags-additional]');

        if (tagsToggle) {
            tagsToggle.addEventListener('click', toggleTagsVisibility.bind(null, tagsContainer));
        }
    },
};
