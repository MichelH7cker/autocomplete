import { ApolloServer } from '@apollo/server';
import { expressMiddleware } from '@apollo/server/express4';
import express from 'express';
import cors from 'cors';
import http from 'http';
import axios from 'axios';

const typeDefs = `#graphql
  type Suggestion {
    text: String!
  }
  
  type Query {
    getSuggestions(term: String!): [Suggestion!]!
  }

  type Mutation {
    incrementScore(term: String!): String
  }
`;

const BACKEND_API_URL = process.env.BACKEND_API_URL || 'http://localhost:8000';

const resolvers = {
  Query: {
    getSuggestions: async (_, { term }) => {
      if (term.length < 4) return [];
      try {
        const response = await axios.get(`${BACKEND_API_URL}/suggestions`, {
          params: { term }
        });
        return response.data;
      } catch (error) {
        console.error('GraphQL Query Error:', error.message);
        throw new Error('Falha ao buscar sugestões no serviço de backend.');
      }
    },
  },
  Mutation: {
    incrementScore: async (_, { term }) => {
      try {
        await axios.post(`${BACKEND_API_URL}/suggestions/increment`, { term });
        return "Success";
      } catch (error) {
        console.error('GraphQL Mutation Error:', error.message);
        throw new Error('Falha ao incrementar score no serviço de backend.');
      }
    },
  },
};

const app = express();
const httpServer = http.createServer(app);

const server = new ApolloServer({
  typeDefs,
  resolvers,
});

await server.start();

const corsOrigin = process.env.CORS_ORIGIN || '*';

app.get('/health', (req, res) => {
  res.status(200).json({ status: 'ok', service: 'graphql-api' });
});

app.use(
  '/graphql',
  cors({ origin: [corsOrigin, 'https://studio.apollographql.com'] }),
  express.json(),
  expressMiddleware(server),
);

await new Promise((resolve) => httpServer.listen({ port: 4000 }, resolve));
console.log(`🚀 GraphQL Server pronto em http://localhost:4000/graphql`);
