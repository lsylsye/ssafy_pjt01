import { computed } from "vue";
import { useRoute } from "vue-router";

export default function useCountry() {
  const route = useRoute();

  const country = computed(() => String(route.params.country || "kr"));
  const apiCountry = computed(() => String(country.value || "kr").toLowerCase());

  return { country, apiCountry };
}
