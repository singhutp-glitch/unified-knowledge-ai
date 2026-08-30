

export function preprocessCitations(markdown) {
    return markdown.replace(
        /\[\s*([\d,\s]+?)\s*\]/g,
        (_, ids) => `<citation ids="${ids}"></citation>`
    );
}