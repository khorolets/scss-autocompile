# Sublime Text 3 SCSS Autocompile
I do like this [less-autocompile package](https://github.com/lohek/less-autocompile) for `Atom`. But I don't like Atom too much. I wanted that plugin for Sublime Text 3. So I've created my own [very first plugin for ST3](https://github.com/khorolets/less-autocompile) inspired by [@lohek](https://github.com/lohek).

I've switched to SCSS and I've decided to adapt my plugin. Here it is.

**Warning!** My plugin has not been tested well and I can't recommend you to use it till I finish it. I'll remove this warning once it is done. I've tested in on *macOS* only for now.


## Dependencies

There is no magic, the plugin uses node's `node-sass-chokidar` to do the job. So it depends on some packages installed globally.

```
npm install -g node-sass-chokidar
```

## Installation

I didn't add my plugin to Sublime Packages so there is only a manual way to install. But this is quite easy to do.

You need to download the plugin and put the folder `SCSSAutocompile` to `Packages` folder of your Sublime Text 3. The `Packages` folder can be found:

 * `~/Library/Application Support/Sublime Text 3/Packages` (macOS)
 * `~/config/sublime-text-3/Packages/` (Linux) **Note** It can be different, depends on the way you've installed Sublime Text 3

## Usage


Add the parameters on the first lines of the LESS file.

```
out (string):  path of CSS file to create
sourcemap (bool): create sourcemap file
compress (bool): compress CSS file
main (string): path to your main LESS file to be compiled
```

### Example

`scss/styles.scss`

```scss
// out: ../css/styles.css
// sourcemap: true
// compress: true

@import "my/components/select.scss";
```

`scss/my/components/select.scss`

```scss
// main: ../../styles.scss

.select {
  height: 100px;
  width: 100px;
}
```

The plugin is being triggered every time `.scss` file is saved.
