<template>
    <div class="resources">
        <h1>Resources</h1>
        <div v-for="resource in resources" :key="resource" class="resource">
            <a :href="resource.url" target="_blank" rel="noopener noreferrer">
                <h4 class="title">{{ resource.title }}</h4>
                <p class="description">{{ resource.description }}</p>
            </a>
        </div>
    </div>
</template>


<script>

export default {
    name: 'ResourcesComponent',
    data() {
        return {
            resources: [
                {
                    title: "Texas Hold'em Utils Python Library", url: "https://pypi.org/project/texas-hold-em-utils/",
                    description: "A python library for simulating a deck of cards, playing games of texas hold em, and providing hand performance statistics."
                },
                {
                    title: "YouTube Channel", url: "https://www.youtube.com/@alexmarkules7316",
                    description: "My YouTube channel where I post videos of my work related to this project and poker analysis."
                },
                {
                    title: "GitHub", url: "https://github.com/amarkules1",
                    description: "My GitHub which includes this project and a few other poker related ropositories (among others)."
                },
                {
                    title: "My Website", url: "http://marqless.xyz/",
                    description: "My personal website with more information about me, my work, and how to get in touch."
                },
            ]
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.resource a {
    color: #fff;
    text-decoration: none !important;
}
.title {
    text-decoration: underline !important;
}
.resource {
    margin-bottom: 40px;
}
</style>