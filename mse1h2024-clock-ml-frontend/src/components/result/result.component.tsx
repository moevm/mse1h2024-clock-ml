import { Link } from "../link/link.component";

import css from "./result.module.css";

export const Result = () => {
	return (
		<section className={css.result}>
			<h1>Ваш результат</h1>
			<img src="" alt="Картинка результата" />
			<p>0/10 баллов</p>
			<Link to="/">Пройти заново</Link>
		</section>
	);
};
