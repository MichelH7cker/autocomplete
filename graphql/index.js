import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';
import axios from 'axios';

const typeDefs = `
  type Suggestion {
    text: String!
  }

  type Query {
    getSuggestions(term: String!): [Suggestion!]!
  }
`;

const BACKEND_API_URL = process.env.BACKEND_API_URL || 'http://localhost:8000';

const resolvers = {
  Query: {
    getSuggestions: async (_, { term }) => {
      // busca somente para caracteres maiores ou iguais a 4
      if (term.length < 4) {
        return [];
      }
      try {
        const response = await axios.get(`${BACKEND_API_URL}/suggestions`, {
          params: { term }
        });
        return response.data;
      } catch (error) {
        console.error('GraphQL: Erro ao buscar sugestões do backend:', error.message);
        return [];
      }
    },
  },
};

const server = new ApolloServer({
  typeDefs,
  resolvers,
});

const { url } = await startStandaloneServer(server, {
  listen: { port: 4000 },
});

console.log(`🚀 GraphQL Server pronto em: ${url}`);
