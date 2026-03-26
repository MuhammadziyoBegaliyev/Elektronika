document.addEventListener("DOMContentLoaded", () => {
    const items = document.querySelectorAll(".parallax-item");

    document.addEventListener("mousemove", (e) => {
        const x = (window.innerWidth / 2 - e.clientX) / 30;
        const y = (window.innerHeight / 2 - e.clientY) / 30;

        items.forEach((item, index) => {
            const depth = (index + 1) * 6;
            const moveX = x * (depth / 10);
            const moveY = y * (depth / 10);

            item.style.transform = `
                translate3d(${moveX}px, ${moveY}px, 0)
                rotateY(${moveX / 2}deg)
                rotateX(${-moveY / 2}deg)
            `;
        });
    });
});