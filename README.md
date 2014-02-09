scholarship-python
==================

A cleaner rewrite of the [old C# scholarship program](https://github.com/day-me-an/scholarship-program) in Jython, which is a language I've gained exposure to since working with [vert.x](http://vertx.io/).

This version focuses on:

* Self-documenting coding style
* [Extract till you Drop](https://sites.google.com/site/unclebobconsultingllc/one-thing-extract-till-you-drop)
* Simplified parallelisation via usage of java.util.concurrent.* (the .net equivelent didn't exist when the original was written).
* Removal of micro-optimisations that made parts of the original unclear.
