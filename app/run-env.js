const dotenv = require('dotenv')
const child_process = require('child_process')

dotenv.config({ path: '../.env' })
const DEV_SERVER_PORT = process.env.PORT_FRONTEND || 4300
const DEV_HOST = process.env['HOST'] || 'localhost'

const child = child_process.exec(`ng serve --port=${DEV_SERVER_PORT} --host=${DEV_HOST}`)
child.stderr.on('data', (err) => console.error(err))
child.stdout.on('data', (data) => console.log(data.toString()))
