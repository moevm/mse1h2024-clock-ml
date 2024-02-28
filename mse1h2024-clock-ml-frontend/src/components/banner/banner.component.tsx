import css from "./banner.module.css";

export const Banner = () => {
	return (
		<section className={css.section}>
			<img className={css.banner} src="./starter.png" alt="Обложка страницы" />
		</section>
	);
};
