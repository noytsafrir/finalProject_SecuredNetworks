import FormLayout from "@/comps/FormLayout";
import "@/styles/globals.css";

export default function App({ Component, pageProps }) {
  return <FormLayout><Component {...pageProps} /></FormLayout>;
}
