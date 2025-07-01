import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';
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
        return [];
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
        return "Error";
      }
    },
  },
};

const server = new ApolloServer({ typeDefs, resolvers });
const { url } = await startStandaloneServer(server, { listen: { port: 4000 } });
console.log(`🚀 GraphQL Server pronto em: ${url}`);
