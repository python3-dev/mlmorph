<template>
  <section>
    <form>
      <input type="number" class="number-input" v-model="input"
      placeholder="Enter a number" @input="onChange" />
     </form>
    <progress v-if="loading" />
    <section v-else class="number-result">
        <h3 class="primary">{{ result && result[0] }}    </h3>
        <h3 class="alternate" v-if="result && result.length>0">{{ result && result[1] }} </h3>
        <h3 class="alternate" v-if="result && result.length>1">{{ result && result[2] }} </h3>
    </section>
  </section>
</template>

<script>
import { ref } from "vue";

const onesStr = [
  "പൂജ്യം",
  "ഒന്ന്",
  "രണ്ട്",
  "മൂന്ന്",
  "നാല്",
  "അഞ്ച്",
  "ആറ്",
  "ഏഴ്",
  "എട്ട്",
  "ഒമ്പത്"
];

const clean = (result) => {
  result = result.replace("<ones><hundreds>", "<hundreds>");
  result = result.replace("<ones><tens>", "<tens>");
  result = result.replace(/^ഒന്ന്<ones><hundreds>/, "<hundreds>");
  result = result.replace(/^ഒന്ന്<ones><thousands>/, "<thousands>");
  return result;
};

const positionValues = (value) => {
  let result = "";
  let crores = value >= 10000000 ? parseInt(value / 10000000) : 0;
  let lakhs = parseInt((value % 10000000) / 100000);
  let thousands = parseInt((value % 100000) / 1000);
  let hundreds = parseInt((value % 1000) / 100);
  let tens = parseInt((value % 100) / 10);
  let ones = parseInt((value % 10) / 1);
  result =
    (crores > 0 ? positionValues(crores) + "<crores>" : "") +
    (lakhs > 0 ? positionValues(lakhs) + "<lakhs>" : "") +
    (thousands > 0 ? positionValues(thousands) + "<thousands>" : "") +
    (hundreds > 0 ? positionValues(hundreds) + "<hundreds>" : "") +
    (tens > 0 ? positionValues(tens) + "<tens>" : "") +
    (ones > 0 ? onesStr[ones] + "<ones>" : "") +
    (value === 0 ? onesStr[ones] + "<zero>" : "");

  return clean(result);
};

export default {
  name: "NumberSpellout",

  setup() {
    const input = ref("");
    const result = ref("");
    const loading = ref(false);

    const onChange = () => {
      let numberMorphemes = positionValues(Number(input.value)) + "<cardinal>";
      spellout(numberMorphemes);
    };

    const spellout = async (numberMorphemes) => {
      loading.value = true;
      try {
        const response = await fetch(
          `/api/generate?word=${encodeURIComponent(numberMorphemes)}`
        );
        const data = await response.json();
        result.value = data.result;
      } catch (error) {
        console.log(error);
      } finally {
        loading.value = false;
      }
    };

    return {
      loading,
      input,
      onChange,
      result,
    };
  },
};
</script>
<style>
.number-input {
  padding: 0.5rem;
  font-size: 1rem;
  font-family: "Manjari", sans-serif;
  line-height: 1.4;
  width: 100%;
  overflow: auto;
  border: 1px solid var(--vp-c-brand);
}

progress {
  width: 100%;
}

.number-result .primary{
 color: var(--vp-c-brand);
}

.number-result .alternate {
  color: var(--vp-c-text-light-2);
}

</style>
