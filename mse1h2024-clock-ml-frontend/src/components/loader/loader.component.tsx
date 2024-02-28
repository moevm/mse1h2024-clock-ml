import css from "./loader.module.css";
export const Loader = () => {
	return (
		<div className={css.wrapper}>
			<div className={css.loader}></div>
			<p>Ожидайте результат</p>
		</div>
	);
};
