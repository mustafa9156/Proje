function kalpTiklandi(element, diziObjesi) {
    let favoriler = JSON.parse(localStorage.getItem("favoriler")) || [];

    // Aynı dizinin adını kontrol et
    const index = favoriler.findIndex(fav => fav.ad === diziObjesi.ad);

    if (index !== -1) {
        // Favorilerden çıkar
        favoriler.splice(index, 1);
        element.style.color = "black";
        element.textContent = "🤍";
    } else {
        // Favorilere ekle
        favoriler.push(diziObjesi);
        element.style.color = "red";
        element.textContent = "❤️";
    }

    localStorage.setItem("favoriler", JSON.stringify(favoriler));
}

document.addEventListener("DOMContentLoaded", () => {
    let favoriler = JSON.parse(localStorage.getItem("favoriler")) || [];

    document.querySelectorAll(".kalp-btn").forEach(el => {
        const diziAd = el.getAttribute("data-ad");
        const favorideVar = favoriler.some(fav => fav.ad === diziAd);

        if (favorideVar) {
            el.style.color = "red";
            el.textContent = "❤️";
        } else {
            el.style.color = "black";
            el.textContent = "🤍";
        }
    });
});
document.addEventListener("DOMContentLoaded", () => {
    const favoriler = JSON.parse(localStorage.getItem("favoriler")) || [];
    document.querySelectorAll(".kalp-btn").forEach(el => {
        const diziAdi = el.getAttribute("data-ad");
        if (favoriler.find(fav => fav.ad === diziAdi)) {
            el.style.color = "red";
            el.textContent = "❤️";
        } else {
            el.style.color = "black";
            el.textContent = "🤍";
        }
    });
});
