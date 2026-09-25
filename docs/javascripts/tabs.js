// Linked content tabs switch every card on the page at once, so cards above
// the one clicked can grow or shrink and push it out from under the pointer.
// Once the switch has settled, scroll by however far the clicked label moved.
document.addEventListener("click", event => {
  const label = event.target.closest(".tabbed-labels > label")
  if (!label)
    return
  const top = label.getBoundingClientRect().top
  requestAnimationFrame(() => requestAnimationFrame(() => {
    const shift = label.getBoundingClientRect().top - top
    if (Math.abs(shift) >= 1)
      window.scrollBy({ top: shift, behavior: "instant" })
  }))
}, true)
