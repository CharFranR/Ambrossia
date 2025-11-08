import anime from "animejs";
export const useAnimateTables = () => {
  return () => {
    anime({
      targets: ".table-card",
      translateX: anime.random(-20, 20),
      translateY: anime.random(-20, 20),
      easing: "easeInOutSine",
      duration: 400,
      direction: "alternate",
    });
  };
};