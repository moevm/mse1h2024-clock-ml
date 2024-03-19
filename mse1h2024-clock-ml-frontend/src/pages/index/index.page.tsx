import { FC } from "react";
import { Layout } from "../../components/layout/layout.component";
import { Banner } from "../../components/banner/banner.component";
import { Link } from "../../components/link/link.component";

export const Index: FC = () => {
	return (
		<Layout>
			<Banner />
			<Link to="/canvas">Начать тестирование</Link>
		</Layout>
	);
};
