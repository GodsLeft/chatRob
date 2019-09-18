const Koa = require('koa');
const fs = require('fs.promised');
const route = require('koa-route');
// 引用静态资源
const path = require('path');
const serve = require('koa-static');
const koaBody = require('koa-body');

const app = new Koa();

const fsstatic = serve(path.join(__dirname, '../'));
app.use(fsstatic)

const main = async ctx => {
    body = ctx.request.body;
    if (!body.input) ctx.throw(400, 'q is required!');
    ctx.response.body = body.input + "--" + "hello";
    // ctx.body = "hello";
};

const about = ctx => {
    ctx.response.body += 'Hello world!';
};

const logger = (ctx, next) => {
    console.log(`${Date.now()} ${ctx.request.method} ${ctx.request.url}`);
    next()
};

const readtmp = async (ctx, next) => {
    ctx.response.body += "wo shi zhuyaguang";
    ctx.response.body = await fs.readfs('./demos/template.html', 'utf-8');
};

const handler = async (ctx, next) => {
    try {
        await next();
    } catch (err) {
        ctx.response.status = err.statusCode || err.status || 500;
        ctx.response.body = {
            message: err.message
        };
    }
};

app.use(koaBody());
app.use(handler);
app.use(logger);
app.use(route.post('/', main));
app.use(route.get('/tmp', readtmp));
app.use(route.get('/about', about));
app.listen(3000);